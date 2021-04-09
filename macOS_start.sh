#!/bin/sh

setUpPkg="default";

function installPkg(){
    echo ${GREEN}"--------------- Start Install ${setUpPkg} ---------------"${NC};
}

function checkOk(){
   if [ $? -eq 0 ]
    then echo ${RED}"---------------Success Install ${setUpPkg} ---------------"${NC};
    else
     echo ${RED}"--------------- Fail Install ${setUpPkg} ---------------"${NC};
     exit 1;
    fi
}

function checkCommandOk(){
   if [ $? -eq 0 ]
    then echo ${RED}"--------------- Success Command for installing ${setUpPkg} ---------------"${NC};
    else
     echo ${RED}"--------------- Fail Command for Installing ${setUpPkg} ---------------"${NC};
     exit 1;
    fi
}

# PKG 파일 설치 기다림
function waitPKG(){
    Installer=$(/bin/ps -e | grep Installer.app | grep -v "grep" | awk '{print $1}')
    echo "PKG installer is not finished."
    while [ $Installer ]
    do
        if [ -z $(/bin/ps -e | grep Installer.app | grep -v "grep" | awk '{print $1}') ]
        then
            break
        fi
    done
}

function installPython(){
    open "./installFile/macOS/python-3.8.7-macosx10.9.pkg"
    checkCommandOk
    waitPKG
    checkCommandOk
}

function install_python(){
    setUpPkg="Python"
    checkCommandOk
    installPkg
    checkCommandOk
    installPython
    checkOk
}

function install_requirement() {
    setUpPkg="Requirement.txt"
    checkCommandOk
    pip3 install -r requirements.txt
    checkCommandOk
}


function install_pip(){
    setUpPkg="pip"
    checkCommandOk
    python3 get-pip.py
}

function main(){
    install_python
    checkCommandOk
    install_pip
    checkOk
    install_requirement
    checkOk
}




#메인 함수 실행
main
