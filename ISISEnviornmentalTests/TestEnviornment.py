import subprocess

def main():
    #subprocess.run("conda activate", shell= True)
    subprocess.call( "conda deactivate", shell= True) 
    


if __name__ == main():
    main()

