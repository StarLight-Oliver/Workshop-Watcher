import subprocess
import os
import json
import requests
import time

def findFiles(dir, files):
    for filename in os.listdir(dir):
        if filename.endswith(".lua"):
            files.append(os.path.join(dir, filename))
        else:
            findFiles(os.path.join(dir, filename), files)

def run_command(command, addonID):

    cmd = ["steamcmd", "+login anonymous" , "+force_install_dir " + os.getcwd(), "+workshop_download_item 4000 " + addonID,"+quit"]

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    if process == None:
        print("Fail")
        return
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            decode = output.strip().decode()
            if ("Success. Downloaded item " + addonID) in decode:
                process.kill()
                break
    newDir = os.getcwd() + "/steamapps/workshop/content/4000/" + addonID + "/"

    print("File Download Complete")

    process = subprocess.Popen(["gmad_linux", newDir + "temp.gma"], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            decode = output.strip().decode()
            if "Done!" == decode:
                process.kill()
                break
    print("File Extraction Complete")

    files = []
    findFiles(newDir + "temp/lua", files)

    repoLoc = os.getcwd() + "/repo/Adware-blocker-gmod/"

    dataFile = repoLoc + "data/adware_block/data.json"

    print("Reading old Data")
    dict = None
    with open(dataFile, "r") as f:
        data = f.read()

        dict = json.loads(data)

    aFiles = []

    for fileName in files:
        aFileName = fileName.replace("/home/move/python/steamapps/workshop/content/4000/" + addonID + "/temp/", "")
        aFiles.append(aFileName)
        dict["timerFiles"][aFileName] = True
        dict["timerFiles"]["addons/gmcpanel-workshop-perged/" + aFileName] = True
    print("Writing New Data")
    with open(dataFile, "w") as f:
        f.write(json.dumps(dict))

    os.system("cd " + repoLoc + "; git add ./data/adware_block/data.json; git commit -a -m ' Updated JSON because of (" + addonID +")'; git push")


    os.system("cd " + newDir + "; rm -rf ./*")

    return aFiles

discordWebhook = "Webhook"

addons = [
    {
        "Name": "SWTOR Prop Pack",
        "Owner": "Tyler",
        "Link": "https://steamcommunity.com/sharedfiles/filedetails/changelog/855631618",
        "Id": "855631618",
        "oldValue": 0
    },
    {
        "Name": "Zhroms Props",
        "Owner": "Tyler",
        "Link": "https://steamcommunity.com/sharedfiles/filedetails/changelog/740395760",
        "Id": "740395760",
        "oldValue": 0
    }
]

oldValue = 0
find1 = '<div class="workshopBrowsePagingInfo">Showing 1-10 of '
find2 = " entries</div>"

while True:
    for addonData in addons:
        r = requests.get(url = addonData["Link"])
        # extracting data in json format
        data = r.text

        position = data.find(find1)
        if position:
            newData = data[position+len(find1):]
            newValue = int(newData)
            if newValue > addonData["oldValue"]:
                r2 = requests.post(url = discordWebhook, data = {"content": addonData["Name"] + " has been updated by " + addonData["Owner"] + ", We will now check for new adverts <@22136437877414297$
                oFiles = run_command("steamcmd", addonData["Id"])
                requests.post(url = discordWebhook, data = {"content": addonData["Name"] + " has these lua files " + json.dumps(oFiles)})

                addonData["oldValue"] = newValue
    time.sleep(300)
