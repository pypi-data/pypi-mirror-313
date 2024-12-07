import os


def gen_script(gb, jar_name):
    beginning = "#!/bin/bash \njava "
    aikars = " --add-modules=jdk.incubator.vector -XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 -XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC -XX:+AlwaysPreTouch -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 -XX:InitiatingHeapOccupancyPercent=15 -XX:G1MixedGCLiveThresholdPercent=90 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem -XX:MaxTenuringThreshold=1 -Dusing.aikars.flags=https://mcflags.emc.gs -Daikars.new.flags=true -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20 "
    mb = int(gb) * 1024
    memory = "-Xms" + str(mb) + "M -Xmx" + str(mb) + "M"
    end = "-jar " + jar_name + " --nogui"
    sh = beginning + memory + aikars + end
    return sh


def write_script(script):
    file = open(r"start.sh", "w")
    file.write(script)
    file.close()


def make_script(gb, jar_name):
    write_script(gen_script(gb, jar_name))
    os.system("chmod a+x " + "start.sh")
