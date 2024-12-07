import asyncio
import io
import socket
import sys
import time
from functools import lru_cache
from email.utils import formatdate
import logging
import ssl
import argparse
from urllib.parse import urlparse, parse_qs

class WSGIServer:
    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM
    request_queue_size = 5
    timeout = 30

    def __init__(self, server_address, application, use_ssl=False, certfile=None, keyfile=None):
        self.listen_socket = socket.socket(self.address_family, self.socket_type)
        self.listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listen_socket.bind(server_address)
        self.listen_socket.listen(self.request_queue_size)
        self.listen_socket.settimeout(self.timeout)

        host, port = self.listen_socket.getsockname()[:2]
        self.server_name = socket.getfqdn(host)
        self.server_port = port
        self.headers_set = []
        self.start_response_called = False

        self.application = application

        self.use_ssl = use_ssl
        if self.use_ssl:
            self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            self.context.load_cert_chain(certfile, keyfile)
        else:
            self.context = None

        logging.basicConfig(level=logging.INFO)

    async def serve_forever(self):
        logging.info(f"Server listening on {self.server_name}:{self.server_port}")
        server = await asyncio.start_server(
            self.handle_request, self.server_name, self.server_port, ssl=self.context
        )
        async with server:
            await server.serve_forever()

    async def handle_request(self, reader, writer):
        start_time = time.time()
        client_address = writer.get_extra_info('peername')
        logging.info(f"New connection from {client_address}")

        try:
            request_line = await self.read_line(reader)
            if not request_line:
                raise ValueError("Empty request or client disconnected.")
            self.parse_request_line(request_line)

            headers = await self.read_headers(reader)
            content_length = int(headers.get('CONTENT_LENGTH', '0'))
            body = b''
            if content_length > 0:
                body = await self.read_body(reader, content_length)

            env = self.get_environ(request_line, headers, body, client_address)
            result = await self.process_request_with_cache(env)
            await self.finish_response(writer, result)
        except asyncio.TimeoutError:
            writer.write(b"HTTP/1.1 408 Request Timeout\r\n\r\n")
        except Exception as e:
            logging.error(f"Error during request handling: {e}")
            writer.write(b"HTTP/1.1 500 Internal Server Error\r\n\r\n")
        finally:
            writer.close()
            await writer.wait_closed()
            end_time = time.time()
            logging.info(f"Request handled in {end_time - start_time:.2f} seconds.")

    async def read_line(self, reader):
        line = await asyncio.wait_for(reader.readline(), timeout=self.timeout)
        return line.decode('latin-1').rstrip('\r\n')

    async def read_headers(self, reader):
        headers = {}
        while True:
            line = await asyncio.wait_for(reader.readline(), timeout=self.timeout)
            if not line or line == b'\r\n':
                break
            line = line.decode('latin-1').rstrip('\r\n')
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            env_key = 'HTTP_' + key.upper().replace('-', '_')
            headers[env_key] = value
            if key.lower() == 'content-length':
                headers['CONTENT_LENGTH'] = value
            if key.lower() == 'content-type':
                headers['CONTENT_TYPE'] = value
        return headers

    async def read_body(self, reader, length):
        body = b''
        remaining = length
        while remaining > 0:
            chunk = await asyncio.wait_for(reader.read(remaining), timeout=self.timeout)
            if not chunk:
                break
            body += chunk
            remaining -= len(chunk)
        return body

    def parse_request_line(self, request_line):
        parts = request_line.split()
        if len(parts) != 3:
            raise ValueError("Malformed request line")
        self.request_method, self.path, self.request_version = parts

    def get_environ(self, request_line, headers, body, client_address):
        parsed = urlparse(self.path)
        qs = parsed.query
        env = {
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': 'https' if self.use_ssl else 'http',
            'wsgi.input': io.BytesIO(body),
            'wsgi.errors': sys.stderr,
            'wsgi.multithread': False,
            'wsgi.multiprocess': False,
            'wsgi.run_once': False,
            'REQUEST_METHOD': self.request_method,
            'PATH_INFO': parsed.path,
            'QUERY_STRING': qs,
            'SERVER_NAME': self.server_name,
            'SERVER_PORT': str(self.server_port),
            'SERVER_PROTOCOL': self.request_version,
            'REMOTE_ADDR': client_address[0],
            'CONTENT_TYPE': headers.get('CONTENT_TYPE', ''),
            'CONTENT_LENGTH': headers.get('CONTENT_LENGTH', '0'),
        }

        for k, v in headers.items():
            if k.startswith('HTTP_'):
                env[k] = v
        return env

    async def process_request_with_cache(self, env):
        cache_key = (env['REQUEST_METHOD'], env['PATH_INFO'], env.get('QUERY_STRING', ''))
        return await self._cached_application(cache_key, env)

    @lru_cache(maxsize=100)
    async def _cached_application(self, cache_key, env):
        return self.application(env, self.start_response)

    def start_response(self, status, response_headers, exc_info=None):
        if self.start_response_called and exc_info is not None:
            raise exc_info[0](exc_info[1]).with_traceback(exc_info[2])
        self.start_response_called = True
        server_headers = [
            ('Date', formatdate(timeval=None, localtime=False, usegmt=True)),
            ('Server', 'WSGIServer Optimized 1.0'),
        ]
        self.headers_set = [status, response_headers + server_headers]

    async def finish_response(self, writer, result):
        status, response_headers = self.headers_set
        response_headers_dict = {h.lower(): v for h, v in response_headers}

        response_body = b''
        if isinstance(result, bytes):
            response_body = result
        else:
            for data in result:
                if isinstance(data, bytes):
                    response_body += data
                else:
                    response_body += data.encode('utf-8')

        if 'content-length' not in response_headers_dict:
            response_headers.append(('Content-Length', str(len(response_body))))

        response_status_line = f'HTTP/1.1 {status}\r\n'
        response_headers_str = '\r\n'.join(f'{header}: {value}' for header, value in response_headers)
        response = response_status_line + response_headers_str + '\r\n\r\n'

        writer.write(response.encode('utf-8'))
        if response_body:
            writer.write(response_body)
        await writer.drain()

def make_server(server_address, application, use_ssl=False, certfile=None, keyfile=None):
    return WSGIServer(server_address, application, use_ssl=use_ssl, certfile=certfile, keyfile=keyfile)

def main():
    parser = argparse.ArgumentParser(description="Run an optimized WSGI server.")
    parser.add_argument('app', help='The WSGI application as module:callable (e.g., myapp:app)')
    parser.add_argument('--host', default='', help='Host to bind to')
    parser.add_argument('--port', type=int, default=8888, help='Port to bind to')
    parser.add_argument('--ssl', action='store_true', help='Use SSL/TLS')
    parser.add_argument('--certfile', help='SSL certificate file')
    parser.add_argument('--keyfile', help='SSL key file')
    args = parser.parse_args()

    module_name, application_name = args.app.split(':')
    module = __import__(module_name)
    application = getattr(module, application_name)

    server_address = (args.host, args.port)
    httpd = make_server(server_address, application, use_ssl=args.ssl, certfile=args.certfile, keyfile=args.keyfile)
    logging.info(f'WSGIServer: Serving HTTP on port {args.port} ...')
    asyncio.run(httpd.serve_forever())

if __name__ == '__main__':
    main()
