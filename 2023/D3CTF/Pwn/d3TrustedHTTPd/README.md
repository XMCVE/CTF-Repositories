Trust me or not, you will never be able to break it~

Attachment:
d3trustedhttpd-attachment.tar.gz

Note: Some sensitive data embedded in the firmware in the chall environment is different from local attachments. Please test it yourself.
HINTS:
1. The flaw of RPC between httpd and trusted_core makes the similarity of Face ID leaked. Can you forge a Face ID to bypass login?
2. Focus on user manage interfaces: <b>TOCTOU</b> in httpd and <b>UAF</b> in TA make you be an Admin! 😼
3. A bad TA may cause memory corruption at CA. Please find vulnerabilities in secure file system (mainly about <b>file-create, file-rename and file-info</b> interfaces).
