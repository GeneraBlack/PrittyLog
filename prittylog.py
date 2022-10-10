import base64
import datetime
import pandas as pd
import logging
logging.basicConfig(filename="logs\\prittylog.log", format='%(asctime)s;%(message)s;%(levelname)s',
                    encoding="utf-8", level=logging.INFO, filemode="w")


class prittylog():
    def __init__(self, modulename="main", isMaster=False):

        self.logger = logging.getLogger()

        self.modulename = modulename
        self.isMaster = isMaster

        ###BASE 64 PNG Logo###
        self.logo = """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"""

    def info(self, message):
        self.logger.info(str(datetime.datetime.now()) + ";" +
                         self.modulename+";"+self.msgcompress(message))

    def warning(self, message):
        self.logger.warning(str(datetime.datetime.now()) + ";" +
                            self.modulename+";"+self.msgcompress(message))

    def error(self, message):
        self.logger.error(str(datetime.datetime.now()) + ";" +
                          self.modulename+";"+self.msgcompress(message))

    def critical(self, message):
        self.logger.critical(str(datetime.datetime.now()) + ";" +
                             self.modulename+";"+self.msgcompress(message))

    def debug(self, message):
        ###Do not use###
        self.logger.debug(str(datetime.datetime.now()) + ";" +
                          self.modulename+";"+self.msgcompress(message))

    def exception(self, message):
        ###Do not use###
        self.logger.exception(str(datetime.datetime.now()) + ";" +
                              self.modulename+";"+self.msgcompress(message))

    def msgcompress(self, message):
        if "-" in message:
            msg = message.split("-", 1)
            return msg[0]+"-"+str(base64.b64encode(msg[1].encode('utf-8')), "utf-8")
        else:
            return message

    def end(self):
        if self.isMaster == True:
            logging.shutdown()
            data = pd.read_csv("logs\\prittylog.log", sep=";",
                               header=None, engine='python')
            jsonlog = data.to_json(orient="index",)
            html = """<!DOCTYPE html>
<header>
    <title>PrittyLog</title>
</header>

<body>
    <div class="headerbar">
        <div class="logo">
            <img class="imglogo" style="display:block; width:100%;" id="base64image"
                src="data:image/png;base64,LOGO</div>
        <div class="logselector">
            <h1>PrittyLog</h1>
            <button class="button-36" role="button" onclick="updatebuttons('All')">All</button>
            <button class="button-36" role="button" onclick="updatebuttons('INFO')">Info</button>
            <button class="button-36" role="button" onclick="updatebuttons('WARNING')">Warning</button>
            <button class="button-36" role="button" onclick="updatebuttons('ERROR')">Error</button>
            <button class="button-36" role="button" onclick="updatebuttons('CRITICAL')">Critical</button>
        </div>
        <div class="filter" id="filter">

        </div>
    </div>
    <div class="content">
        <div class="logs" id="logs">

        </div>
        <div class="logdetails" id="logdetails">

        </div>
    </div>
</body>
<script>
    let login = JSON.parse('PYTHONJSONLOG');
    let selectedmodulesin = "All";
    let selectedcategroyin = "All";
    let filterresult = filter(selectedmodulesin, selectedcategroyin, login);
    document.getElementById('logs').innerHTML = loop(filterresult);

    document.getElementById('filter').innerHTML = buildselector(onlyUnique(login))

    function updateDetails(filterresult, id) {
        document.getElementById('logdetails').innerHTML = details(filterresult, id);
    }
    function updatemodule(module) {
        selectedmodulesin = module;
        filterresult = filter(selectedmodulesin, selectedcategroyin, login);
        document.getElementById('logs').innerHTML = loop(filterresult);
    }

    function updatebuttons(value) {
        selectedcategroyin = value;
        filterresult = filter(selectedmodulesin, selectedcategroyin, login);
        document.getElementById('logs').innerHTML = loop(filterresult);
    }

    function buildselector(modules) {
        let html = "<div><select class='classic' id='moduleselector' style='width: 100%' onchange='updatemodule(this.value)'><option selected=''> Please Select Module</option>";
        for (const i in modules) {
            html += "<option value='" + modules[i] + "'>" + modules[i] + "</option>";
        }
        html += "</select></div>";
        return html;
    }

    function onlyUnique(log) {
        let modules = ['All'];
        for (const i in log) {
            modules.push(log[i][2])
        }
        return modules.filter(oUfilter);
    }
    function oUfilter(value, index, self) {
        return self.indexOf(value) === index;
    }

    function filter(selectedmodules, selectedcategroy, log) {
        let filtered = [];
        if (selectedmodules == "All" && selectedcategroy != "All") {
            for (const i in log) {
                if (selectedcategroy.includes(log[i][4])) {
                    filtered.push(log[i]);
                    console.log("A" + log[i]);
                }
            }
        } else if (selectedcategroy == "All" && selectedmodules != "All")

            for (const i in log) {
                if (selectedmodules.includes(log[i][2])) {
                    filtered.push(log[i]);
                    console.log("B" + log[i]);
                }
            }
        else if (selectedmodules == "All" && selectedcategroy == "All") {
            for (const i in log) {

                filtered.push(log[i]);
                console.log("C" + log[i]);
            }
        }
        else {
            for (const i in log) {
                if (selectedmodules.includes(log[i][2]) && selectedcategroy.includes(log[i][4])) {
                    filtered.push(log[i]);
                    console.log("D" + log[i]);
                }
            }
        } return filtered;
    }


    function wrapper(date, module, message, category, position) {
        let delimiter = "-"
        if (message.includes(delimiter)) {
            var mg = message.split("-");
        }
        else {
            var mg = [message];
        }

        return `<div class="log${category}">
                    <div class="Subject">${category} - ${module} - ${date}</div>
                    <div class="message">${mg[0]}</div> <button class="todetails" onclick="updateDetails(filterresult,${position})"> Show Details</button>
                </div >`;
    }
    function loop(filtered) {
        let html = "";
        for (const i in filtered) {
            html += wrapper(filtered[i][0], filtered[i][2], filtered[i][3], filtered[i][4], i);
        }
        return html;
    }
    function details(filterresult, position) {
        let delimiter = "-"
        if (filterresult[position][3].includes(delimiter)) {
            var mg = filterresult[position][3].split("-");

            return `<div class="details">
                    <div class="Subject"><h1>${filterresult[position][4]} - ${filterresult[position][2]} - ${filterresult[position][1]}</h1></div>
                    <div class="message"><h2>${mg[0]}</h2></div >
                    <div class="mdetail">${decodeURIComponent(escape(window.atob(mg[1])))}</div ></div>`;
        }
        else {
            var mg = [filterresult[position][3]];
            return `<div class="details">
                    <div class="Subject"><h1>${filterresult[position][4]} - ${filterresult[position][2]} - ${filterresult[position][1]}</h1></div>
                    <div class="message"><h2>${mg[0]}</h2></div ></div>`;
        }

    }
</script>
<style>
    .todetails {
        float: right;
    }

    .logDEBUG {
        background-color: #00ff00af;
        border-color: black;
        border-style: inset;
        border-width: 2px;
        border-radius: 15px;
        padding: 5px;
        margin: 2px;
    }

    .logINFO {
        background-color: #0000ffaf;
        padding: 5px;
        border-color: black;
        border-style: inset;
        border-width: 2px;
        border-radius: 15px;
        margin: 2px;
    }

    .logWARNING {
        background-color: #ffff00af;
        border-color: black;
        border-style: inset;
        border-width: 2px;
        border-radius: 15px;
        padding: 5px;
        margin: 2px;
    }

    .logERROR {
        background-color: #ff0000af;
        border-color: black;
        border-style: inset;
        border-width: 2px;
        border-radius: 15px;
        padding: 5px;
        margin: 2px;
    }

    .logCRITICAL {
        background-color: #ff00ffaf;
        border-color: black;
        border-style: inset;
        border-width: 2px;
        border-radius: 15px;
        padding: 5px;
        margin: 2px;
    }

    .logs {
        width: 50%;
        float: left;
        height: 100%;
        overflow: auto;
        background: rgb(228, 245, 252);
        background: -moz-linear-gradient(45deg, rgba(228, 245, 252, 1) 0%, rgba(191, 232, 249, 1) 50%, rgba(159, 216, 239, 1) 51%, rgba(42, 176, 237, 1) 100%);
        background: -webkit-linear-gradient(45deg, rgba(228, 245, 252, 1) 0%, rgba(191, 232, 249, 1) 50%, rgba(159, 216, 239, 1) 51%, rgba(42, 176, 237, 1) 100%);
        background: linear-gradient(45deg, rgba(228, 245, 252, 1) 0%, rgba(191, 232, 249, 1) 50%, rgba(159, 216, 239, 1) 51%, rgba(42, 176, 237, 1) 100%);
        filter: progid:DXImageTransform.Microsoft.gradient(startColorstr='#e4f5fc', endColorstr='#2ab0ed', GradientType=1);
        flex-direction: column;
        border-color: black;
        border-style: inset;
        border-width: 2px;
        border-radius: 0px;
        overflow: scroll;
        display: flex;
        height: calc(100vh - 150px);
    }

    .content {
        display: flex;
    }


    .logdetails {
        float: right;
        display: flex;
        padding-left: 5px;
        width: 50%;
        height: 100%;
        overflow: auto;
        background: rgb(228, 245, 252);
        background: -moz-linear-gradient(45deg, rgba(228, 245, 252, 1) 0%, rgba(191, 232, 249, 1) 50%, rgba(159, 216, 239, 1) 51%, rgba(42, 176, 237, 1) 100%);
        background: -webkit-linear-gradient(45deg, rgba(228, 245, 252, 1) 0%, rgba(191, 232, 249, 1) 50%, rgba(159, 216, 239, 1) 51%, rgba(42, 176, 237, 1) 100%);
        background: linear-gradient(45deg, rgba(228, 245, 252, 1) 0%, rgba(191, 232, 249, 1) 50%, rgba(159, 216, 239, 1) 51%, rgba(42, 176, 237, 1) 100%);
        filter: progid:DXImageTransform.Microsoft.gradient(startColorstr='#e4f5fc', endColorstr='#2ab0ed', GradientType=1);
        border-color: black;
        border-style: inset;
        border-width: 2px;
        border-radius: 0px;
        overflow: scroll;
        height: calc(100vh - 150px)
    }

    .headerbar {
        background: rgb(228, 245, 252);
        background: -moz-linear-gradient(45deg, rgba(228, 245, 252, 1) 0%, rgba(191, 232, 249, 1) 50%, rgba(159, 216, 239, 1) 51%, rgba(42, 176, 237, 1) 100%);
        background: -webkit-linear-gradient(45deg, rgba(228, 245, 252, 1) 0%, rgba(191, 232, 249, 1) 50%, rgba(159, 216, 239, 1) 51%, rgba(42, 176, 237, 1) 100%);
        background: linear-gradient(45deg, rgba(228, 245, 252, 1) 0%, rgba(191, 232, 249, 1) 50%, rgba(159, 216, 239, 1) 51%, rgba(42, 176, 237, 1) 100%);
        filter: progid:DXImageTransform.Microsoft.gradient(startColorstr='#e4f5fc', endColorstr='#2ab0ed', GradientType=1);
        height: 150px;
        width: 100%;
        display: flex;
    }

    .logo {

        height: 150px;
        width: 150px;
        float: left;
    }

    .filter {

        height: 150px;
        width: 250px;
        float: right;

    }

    .imglogo {
        position: relative;
        margin: auto;
        top: 50%;
        left: 50%;
        right: 0;
        bottom: 0;
        -ms-transform: translate(-50%, -50%);
        transform: translate(-50%, -50%);
    }

    .button-36 {
        background-image: linear-gradient(92.88deg, #455EB5 9.16%, #5643CC 43.89%, #673FD7 64.72%);
        border-radius: 8px;
        border-style: none;
        box-sizing: border-box;
        color: #FFFFFF;
        cursor: pointer;
        flex-shrink: 0;
        font-family: "Inter UI", "SF Pro Display", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
        font-size: 16px;
        font-weight: 500;
        height: 4rem;
        padding: 0 1.6rem;
        text-align: center;
        text-shadow: rgba(0, 0, 0, 0.25) 0 3px 8px;
        transition: all .5s;
        user-select: none;
        -webkit-user-select: none;
        touch-action: manipulation;
    }

    .button-36:hover {
        box-shadow: rgba(80, 63, 205, 0.5) 0 1px 30px;
        transition-duration: .1s;
    }

    @media (min-width: 500px) {
        .button-36 {
            padding: 0 50px;
        }
    }

    select {

        /* styling */
        background-color: white;
        border: thin solid blue;
        border-radius: 4px;
        font: inherit;
        display: flex;
        line-height: 1.5em;
        padding: 0.5em 3.5em 0.5em 1em;

        /* reset */

        margin: 0;
        -webkit-box-sizing: border-box;
        -moz-box-sizing: border-box;
        box-sizing: border-box;
        -webkit-appearance: none;
        -moz-appearance: none;
    }

    select.classic {
        background-image:
            linear-gradient(45deg, transparent 50%, blue 50%),
            linear-gradient(135deg, blue 50%, transparent 50%),
            linear-gradient(to right, skyblue, skyblue);
        background-position:
            calc(100% - 20px) calc(1em + 2px),
            calc(100% - 15px) calc(1em + 2px),
            100% 0;
        background-size:
            5px 5px,
            5px 5px,
            2.5em 2.5em;
        background-repeat: no-repeat;
    }

    .logselector {
        text-align: center;

        flex: 1;
    }
</style>"""
        prittylog = html.replace("PYTHONJSONLOG", jsonlog)
        logfile = open("logs\\prittylog.html", "w")
        logfile.write(prittylog.replace("LOGO", self.logo))
        logfile.close()
