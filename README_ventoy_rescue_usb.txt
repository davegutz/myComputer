# Full installs
ubuntu-24.04.3-desktop-amd64.iso
lubuntu-24.04.3-desktop-amd64.iso
pop-os_22.04_amd64_intel_57.iso


# Create windows rescue iso (for simple repairs without full install above)
To put Windows PE (WinPE) on a Ventoy USB, create a WinPE ISO file using Microsoft's /navWindows ADK and the WinPE add-on, then simply copy the generated ISO file directly to the Ventoy partition on the USB drive.

	This YouTube tutorial is awesome.  It is slightly different tha	n following in that it installs to default locations.

		https://www.youtube.com/watch?v=kQ9QH3J-Rps&t=9s
		Start 'Deployment and Imaging Tools Environment' as administrator
		prompt $g
		copype
		mkdir c:\winPE
		copype amd64 c:\winPE\WinPE_x64  
		Makewinpemedia /iso c:\winpe\WinPE_x64 c:\winPE\WinPE_x64.iso   
		cd c:\winPE     
		dir  # confirm that .iso made
		copy to ventoy

	Use the Windows PE Command Prompt:

		Once booted, the Windows PE environment will start automatically, and you will see a command prompt. 

		The wpeinit command initializes Windows PE, setting up basic drivers and networking. 

		Use built-in command-line tools like:

		DiskPart: to manage disks, partitions, and volumes. 

		DISM: (Deployment Image Servicing and Management) to capture and manage Windows images. 

		BCDboot: for adding boot entries. 

		You can also run batch files, scripts, and custom applications


# ProtonVPN 
	# for Windows (on ventoy)
		ProtonVPN_v4.3.1_x64.exe

	# for Linux deb (ubuntu - based)
		wget https://repo.protonvpn.com/debian/dists/stable/main/binary-all/protonvpn-stable-release_1.0.8_all.deb

	# or
		# visit the site
	# or copy off ventoy
	
		# Install Linux
			sudo dpkg -i ./protonvpn-stable-release_1.0.8_all.deb && sudo apt update

# Utilities
	# find devices and open ports
		nmap

	# dns jump -  lets you quickly test and switch between multiple DNS servers like Cloudflare's 1.1.1.1, Google DNS, etc., to see which one works best for your use case
		DnsJumper   # windows only
		
	# netresview - windows only.  Not sure it works on Windows 11
		NetResView.exe
		
	# Medicat for Windows
		to create the iso that is in ventoy, install medicat locally on windows
		What You Can Do with the Toolkit
			Perform Data Recovery: Recover lost or deleted files and partitions. 

			Reset Passwords: Unlock computers by resetting user account passwords. 
			
			Scan for Malware: Use included antivirus tools to remove viruses and other malicious software. 

			Run Diagnostics: Check hard drives for errors and test system memory. 

			Backup Data: Create backups of important files before making significant changes to the system. 

			Troubleshoot System Issues: Access the command prompt, run system file checkers, or perform other repairs on the operating system
		
	# Rescatux for Linux
		Features
			Restore GRUB and GRUB2
			(>=0.41 beta 1) Create a new UEFI Boot entry
			(>=0.41 beta 1) Fake Microsoft Windows UEFI
			(>=0.41 beta 1) Reinstall Microsoft Windows EFI
			(>=0.41 beta 1) Update UEFI order
			(>=0.31 beta 4) Update any GRUB2 menues
			Update Debian/Ubuntu grub menues
			Clear Windows passwords
			Restore Windows MBR (BETA)
			(>=0.31 beta 4) Promote a Windows user to Administrator role
			Change Gnu/Linux Password
			Regenerate sudoers file
			File System Check (Forced Fix) (BETA)
			(>= 0.40 beta 1) SELinux based systems are supported
			(>=0.31 beta 3) boot-repair 3.199
			(>=0.31 beta 1) Gparted 0.12
			(>=0.31 beta 3) os-uninstaller 3.199
			(>=0.31 beta 3) clean-ubiquity 3.199
			(>=0.31 beta 3) photorec
			(>=0.31 beta 3) testdisk 6.13
			(>=0.31 beta 1) Gpart 0.1h-11+b1
			(>=0.31 beta 1) extundelete 0.2.0
			(>=0.40 beta 2) Gptsync - Create Hybrid MBR
			(>=0.40 beta 2) Recompute Hybrid GPT/MBR CHS
			(>=0.40 beta 2) Check bios_grub partition on GPT
			Boot Info Script
			Share a log (Support)
			Share a log on forum (Support)
			Show logs (Support)
			(>=0.41 beta 1) UEFI Partition Status
			(>=0.41 beta 1) Hide Microsoft Windows UEFI
			(>=0.41 beta 1) Check UEFI Boot


		