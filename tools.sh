
# init 函数
function init() {
    sudo apt install python3.11-venv
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
   
}

# clear 函数
function clear() {
    # 清除 venv
    rm -rf venv
    # 清除 __pycache__
    find . -name "__pycache__" | xargs rm -rf
    # 清除 migrations 里的迁移文件但是不清除 __init__.py
    find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
 

}


if [[ "$1" == "clear" ]]; then
    clear
fi

if [[ "$1" == "init" ]]; then
    init
fi