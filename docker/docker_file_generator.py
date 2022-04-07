from asyncore import read
import os,sys,json
'''
the folder containes all .py files & requirements.txt
the container name for specific module is passed as argument eg:/appmanager
the scriptfile has all run commands to run the folder contents in order
'''
def generate_dockerfile(port,folder,file):
    f=open("."+folder+"/Dockerfile","w")
    destination="/app"
    # f.write("FROM alpine:latest\nRUN echo \"** install Python **\" && \\\napk add --no-cache python3 && \\\nif [ ! -e /usr/bin/python ]; then ln -sf python3 /usr/bin/python ; fi && \\\necho \"** install pip **\" && \\\npython3 -m ensurepip && \\\nrm -r /usr/lib/python*/ensurepip && \\\npip3 install --no-cache --upgrade pip setuptools wheel && \\\nif [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi\n")
    f.write("FROM ubuntu:20.04\nRUN apt-get update\nRUN apt-get install -y python3-pip\n")
    f.write("WORKDIR /app\n")
    # entries=os.listdir(os.getcwd())
    f.write("COPY . /app\n")
    # for filename in entries:
    #     if filename=="Dockerfile":
    #         continue
    #     f.write("COPY "+filename+" "+destination+"/\n")
    f.write("RUN pip3 install -r requirements.txt\n")
    # f.write("COPY "+data['appfolderpath']+" "+data['appfolderpath']+"/image\n")
    f.write("EXPOSE "+port+"\n")
    # f.write("ENTRYPOINT [./]\n")

    # '''generate_script_file()'''
    # sfile=open("scriptfile.sh","w")
    # sfile.write("#!/bin/bash\n")
    # for cmd in data['listOffiles']:
    #     sfile.write("python3 "+cmd+"\n")
    # f.write("RUN chmod +x scriptfile.sh\n")    
    f.write("CMD python3 "+file)

    # if os.path.exists("scriptfile.sh"):
    #     os.remove("scriptfile.sh")
    # else:
    #     print("The file does not exist")
    
generate_dockerfile(sys.argv[1],sys.argv[2],sys.argv[3])




