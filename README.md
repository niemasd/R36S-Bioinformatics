# R36S-Bioinformatics
A suite of Bioinformatics tools for the [R36S](https://handhelds.miraheze.org/wiki/R36S_Handheld_Wiki).

# Installation
1. Install the [ArkOS](https://handhelds.miraheze.org/wiki/R36S_Custom_Firmware#ArkOS_Community_Maintained_Image) image if you haven't already
    * This might not be necessary, but it's what I'm using (and it's better than the stock R36S image)
2. Connect the R36S to the internet
    * You can use a [wireless USB dongle](https://github.com/dov/r36s-programming/tree/main?tab=readme-ov-file#connecting), or you can use USB tethering via a smartphone
3. [SSH](https://github.com/dov/r36s-programming/tree/main?tab=readme-ov-file#ssh) into the R36S
    * On the R36S, go to "Options", then click "Enable Remote Services"
    * If you have internet connection when you do this, it'll enable remote services and show you the IP address of the R36S
    * SSH into that IP address
4. While in the home directory (`~`), clone this repository: `git clone https://github.com/niemasd/R36S-Bioinformatics.git`
5. Run the installation script: `./R36S-Bioinformatics/install.sh`

# Apps
After following the installation steps, you should now have a "Bioinformatics" console, which is where the R36S-Bioinformatics apps will reside:

* `FASTTREE`: Infer a phylogeny from a multiple sequence alignment using [FastTree](https://morgannprice.github.io/fasttree/)
* `FILE_BROWSER`: Browse the file system of the device
* `HELLO_WORLD`: Test the button inputs on the device
* `INSTALL`: Rerun the installation script
* `MINIMAP2`: Map reads against a reference genome using [Minimap2](https://github.com/lh3/minimap2)
* `NEWICK_VIEWER`: View a Newick tree using the `nw_display` tool from [Newick Utilities](https://github.com/tjunier/newick_utils)
* `TEXT_VIEWER`: View a plain-text file
* `UPDATE_APPS`: Update all R36S-Bioinformatics apps (this will also automatically pull any new apps)
* `UPDATE_SYSTEM`: Update all system dependencies (not bioinformatics tools)
* `VIRALMSA`: Perform multiple sequence alignment using [ViralMSA](https://github.com/niemasd/ViralMSA) wrapping around [Minimap2](https://github.com/lh3/minimap2)
* `VIRAL_CONSENSUS`: Call a consensus sequence from mapped reads using [ViralConsensus](https://github.com/niemasd/ViralConsensus)
