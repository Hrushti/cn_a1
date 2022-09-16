# Computer Networks: Assignment 1

The pdfs cn_a1_p1.pdf, cn_a1_p2.pdf, and cn_a1_p3.pdf contain answers to the respective parts.

#### Steps to run

1. Install all required packages (`socket`, `os`)
2. Clone this repository on your machine
3. There are two separate folders under p1: client and server.
4. Open these folders in separate terminals, and run conn_s.py and conn_c.py, in this order.
5. The connection will be established.
6. On the client side, you can now execute commands.
7. As a sample, the data folder contains a text file alice.txt, which can be downloaded to the client, and then uploaded to the server in a different folder.
8. To use the different encrytion modes, use `-pt` (for plain text), `-tp` (for transpose) or `-sb` (for subtstitution encoding) after the file name. Example:
` dwd alice.txt -tp ` or ` upd alice.txt -pt `. If no encryption is provided, plain-text is used by default.
9. (note) downloading and uploading files does not delete them from the original locations.
