# R36S-Bioinformatics
A suite of Bioinformatics tools for the [R36S](https://handhelds.miraheze.org/wiki/R36S_Handheld_Wiki).

# Installation

1. Connect the R36S to the internet: https://github.com/dov/r36s-programming/tree/main?tab=readme-ov-file#connecting
  * You can use a wireless USB dongle, or you can use USB tethering via a smartphone
2. SSH into the R36S: https://github.com/dov/r36s-programming/tree/main?tab=readme-ov-file#ssh
  * On the R36S, go to "Options", then click "Enable Remote Services"
  * If you have internet connection when you do this, it'll enable remote services and show you the IP address of the R36S
  * SSH into that IP address
3. While in the home directory (`~`), clone this repository: `git clone https://github.com/niemasd/R36S-Bioinformatics`
4. Run the installation script: `./R36S-Bioinformatics/install.sh`
