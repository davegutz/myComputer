# Full installs
ubuntu-24.04.3-desktop-amd64.iso
lubuntu-24.04.3-desktop-amd64.iso
pop-os_22.04_amd64_intel_57.iso

# Tool images
gparted-live-1.7.0-8-amd64.iso
systemrescue-12.02-amd64.iso
imageUSB_MemTest86_v11.5_bld1000  # weeds out bad ram

# gparted-live-1.7.0-8-amd64.iso
GParted is a bootable partition editor you can use to shrink, expand, and move partitions in an environment that's fully removed from your storage. This is an extremely useful tool for fixing broken dual-boot setups or expanding a stubborn partition. I actually used this just the other day to expand my primary C: drive partition after upgrading to a larger SSD. You can do so using its pretty intuitive GUI interface, which is quite easy to use. GParted is a mainstay in my toolkit, and it should be in yours as well.


# clonezilla
 "How do I clone my OS to a new drive" is a question that so many users have and struggle with solving, especially on the Windows side of things. Cloning drives can be a huge hassle, especially when you only have one device to work with, but it really doesn't have to be that way.

Clonezilla is partition and disk image migration software that can be easily used to do just that, and so much more. The live version can be booted from a USB, and is super lightweight. For individual users, this is the way you clone your old drive to your new one, but for admins of multiple systems, you can use Clonezilla to image many systems at the same time. The local drive to drive cloning has been massively helpful many times, and is definitely something that should be on one of your USB sticks.

# systemrescue is an all purpose image that:
SystemRescue is a distro built exactly for these moments. It includes a collection of system repair utilities, including GParted, TestDisk, fsarchiver, ddrescue, and more. These tools work with both Windows and Linux, and SystemRescue does a great job of offering a repair environment that can help bring your PC back to life.

The distro works on both BIOS and UEFI systems and handles all major filesystems, including ext4, XFS, Btrfs, NTFS, and network file systems like Samba and NFS. It's the distro you hope you never have to use but would be grateful to have when things go wrong.


# MemTest86 - weeds out bad RAM
If you're doing any kind of RAM overclocking, tuning of timings, or just looking to ensure there's nothing wrong with your memory, MemTest86 is a necessary tool to have at the ready. Memory issues are really difficult to pin down, and if you're only working at the OS level, you'll struggle to really get to the bottom of it. Running MemTest86 overnight will weed out suspected bad DIMMs and even help validate XMP/EXPO setups.


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


		