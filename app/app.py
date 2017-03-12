from flask import Flask, render_remplate

@application.route('/')
def showMachineList():
    return render_template("list.html")

if __name__ == "__main__":
    application.run(host='0.0.0.0')