import subprocess

for i in range(0,500):
    job = "sbatch jobscript" + str(i) + ".sh"
    print(job)
    p = subprocess.Popen(job, shell=True)
    if p.wait() != 0:
        print("error!")
print("all done")
