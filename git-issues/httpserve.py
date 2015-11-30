#!/usr/bin/env python
import BaseHTTPServer
import os
import re

class GitIssues(BaseHTTPServer.BaseHTTPRequestHandler):

    repos_dir_in_home = os.path.expanduser("~/.git-issues/")

    def html_200(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def html_404(self):
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write("""<!DOCTYPE html>
                            <h3>Error loading the page</h3>
                        """)

    def json_200(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        f = None
        if self.path == "/":
            try:
                f = open("site/index.html", 'r')
                self.html_200()
                self.wfile.write(f.read())
            except Exception:
                self.html_404()

            finally:
                if f is not None:
                    f.close()
        elif '.js' in self.path or '.css' in self.path \
            or '.woff' in self.path or '.ttf' in self.path:
            try:
                path = self.path
                try:
                    path = self.path[:self.path.index('?')]
                except:
                    # Throwing an error seems like an interesting choice but
                    # this is what is reality...
                    pass
                f = open("site/{0}".format(path))
                self.send_response(200)
                if '.js' in self.path:
                    self.send_header('Content-type', 'text/js')
                elif '.woff' in self.path:
                    self.send_header('Content-type', 'text/woff')
                elif '.ttf' in self.path:
                    self.send_header('Content-type', 'text/ttf')
                elif '.css' in self.path:
                    self.send_header('Content-type', 'text/css')
                else:
                    self.send_header('Content-type', 'text')
                self.end_headers()
                self.wfile.write(f.read())
            except Exception as e:
                self.html_404()
            finally:
                if f is not None:
                    f.close()

        elif re.search("(repo=(.*))", self.path):
            repo_matches = re.search("(repo=(.*))", self.path)

            try:
                f = open("{0}/{1}.json".format(self.repos_dir_in_home, repo_matches.group(2)), 'r')
                self.json_200()
                self.wfile.write(f.read())
            except Exception:
                self.json_200()
                self.wfile.write('{"error":"Repository file not found."}')
            finally:
                if f is not None:
                    f.close()


def main():
    try:
        repos_dir_in_home = os.path.expanduser("~/.git-issues/")
        server = BaseHTTPServer.HTTPServer(('', 5678), GitIssues)
        print("Starting Server on http://localhost:5678/")
        repo_files = [f for f in os.listdir(repos_dir_in_home) \
                      if os.path.isfile(os.path.join(repos_dir_in_home, f))]
        for repos in repo_files:
            print("http://localhost:5678/?repo={0}".format(repos.replace(".json", "")))
        server.serve_forever()
    except KeyboardInterrupt:
        print("^C received, shutting down the server")
        server.socket.close()

if __name__ == '__main__':
    main()
