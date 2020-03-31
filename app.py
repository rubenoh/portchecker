from flask import Flask, render_template, request
import pandas
import checkports

app = Flask(__name__)

@app.route("/")
def home():
    return "Communucation Check for k8s "

@app.route("/portchecker")
def port_check():
    final = checkports.checkfunction()
    df = pandas.DataFrame(final)
    df.to_csv("results.csv", index=None)
    df = pandas.read_csv("results.csv" )
    ip_origin=checkports.get_IP()
    return render_template('view.html', tables=[df.to_html(index=False)], titles=["na", ip_origin])
    #return df.to_html(index=False)


@app.route("/troubleshooting/")
def hello_there():
    place_ip = request.args.get("ip", default=None)
    place_port = request.args.get("port", default=None)
    place_protocol = request.args.get("protocol", default=None)
    if place_ip and place_port and place_protocol:
        content = checkports.function_troubleshoot(place_ip, place_port, place_protocol)
        df = pandas.DataFrame(content)
        df.to_csv("results.csv", index=None)
        df = pandas.read_csv("results.csv")
        ip_origin=checkports.get_IP()
        return render_template('view.html', tables=[df.to_html(index=False)], titles=["na", ip_origin])
    else:
        content = "Format doesn't match the correct pattern, try url in the following form: troubleshooting/?ip=ipvalue&port=portvalue&protocol=tcp or udp"    
    
    return content

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)