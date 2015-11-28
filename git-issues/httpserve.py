#!/usr/bin/env python
import BaseHTTPServer
import os
import re

class GitIssues(BaseHTTPServer.BaseHTTPRequestHandler):

    repos_dir_in_home = os.path.expanduser("~/.git-issues/")

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Need to handle each different repo
        repo_matches = re.search("(repo=(.*))", self.path)
        f = None
        try:
            f = open("{0}/{1}.json".format(self.repos_dir_in_home, repo_matches.group(2)), 'r')
            self.wfile.write(f.read())
        except Exception:
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
