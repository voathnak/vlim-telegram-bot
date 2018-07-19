import subprocess


class NGINXConfig:

    def __init__(self):
        pass

    def create(self, server_name, proxy_pass, file_name, file_path="/etc/nginx/sites-available/",
                 target_path="/etc/nginx/sites-enabled/"):
        server_name = server_name.strip()
        file_path = file_path.strip()
        file_name = file_name.strip()
        file = "%s%s" % (file_path, file_name.strip())
        proxy_pass = proxy_pass.strip()
        port = proxy_pass.split(':')[1]
        target_path = target_path.strip()
        target_file = "%s%s" % (target_path, file_name)

        lines = [
            'rm %s' % file,
            'echo "server {                                           " >> %s' % file,
            'echo "  listen 80;                                       " >> %s' % file,
            'echo "  server_name %s;                                  " >> %s' % (server_name, file),
            'echo "                                                   " >> %s' % file,
            'echo "  access_log /var/log/nginx/%s.access.log;         " >> %s' % (server_name, file),
            'echo "  error_log /var/log/nginx/%s.error.log;           " >> %s' % (server_name, file),
            'echo "                                                   " >> %s' % file,
            'echo "  location / {                                     " >> %s' % file,
            'echo "   proxy_pass              %s;                     " >> %s' % (proxy_pass, file),
            'echo "   proxy_set_header        Host \$host;             " >> %s' % file,
            'echo "   proxy_set_header        X-Real-IP \$remote_addr; " >> %s' % file,
            'echo "   proxy_set_header        X-Forwarded-For \$proxy_add_x_forwarded_for; " >> %s' % file,
            'echo "   proxy_connect_timeout   350;                                        " >> %s' % file,
            'echo "   proxy_next_upstream error timeout invalid_header http_500 http_502 http_503 http_504;" >> %s' %
            file,
            'echo "   proxy_send_timeout      400;                    " >> %s' % file,
            'echo "   proxy_buffers           16 64k;                 " >> %s' % file,
            'echo "   client_max_body_size    100m;                   " >> %s' % file,
            'echo "   client_body_buffer_size 128k;                   " >> %s' % file,
            'echo "  }                                                " >> %s' % file,
            'echo "                                                   " >> %s' % file,
            'echo "}                                                  " >> %s' % file,
            'ln -s %s %s' % (file, target_file),
            'ufw allow %s' % port,
            'service nginx restart',

        ]

        for line in lines:
            # print "echo 'jR6hZKQUZ8ig' | sudo -SH -u vlim-bot bash -c '%s'" % line
            subprocess.call("echo 'jR6hZKQUZ8ig' | sudo -SH -u vlim-bot bash -c '%s'" % line, shell=True)
