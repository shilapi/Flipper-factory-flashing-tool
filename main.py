import sys
import os
import time
import logging
import colorlog
import yaml
import subprocess
from Crypto.Cipher import AES

config = yaml.safe_load(open("config.yaml"))

logger = logging.getLogger()


sh = colorlog.StreamHandler()
formatter = colorlog.ColoredFormatter(
    "%(log_color)s%(asctime)s [%(funcName)s]: %(message)s"
)
sh.setFormatter(formatter)
logger.addHandler(sh)
logger.setLevel(logging.INFO)

python_path = sys.executable
script_time = time.strftime("%Y_%m_%d-%H_%M_%S")
banner = """
         @@@#.  .-@@@@                                  @@*                        @  
     @@@-             .@@@                            @@     .....:::... ...  .:.  @  
.#@@+     ::..:......     @@    #@@@@@@@ @@==+===@@@@@@   ........   :..........:  @  
 .    ..=:.   .... ..:::.   @@=:..      ..              . ..... .:::...:-.-=..==  .@  
   :...-.....:..::....  ...        .:.........-: ........:.. ...-.... ...-......  @   
   .:..-........=:.:=.:.:.::...:  -: ......... ..  ........:..  .:-.....:-....   @    
 ...=.. --.:::-= .....::.......  =: ............ @  ...  .....:: ..:===-.. ..  %@     
 ==:.............. ......  ....  @  ............  @  ..=:  ....:.. ........   @@      
 ............   .:......  =:..  @  .............  %@ ....=.  ..........    -@@        
:-           == ......  :=  .. =  ...............  @  ... ==  .....::.-*@@@@          
 @@@@@@@@@@@ @. .....  =....   @  ................  * ...   @  .......@               
            @  .....  =:.. . .@@ .................  @   ...  @. ..... .@              
           @  .....  =. .:  =@ @ .................  %@. ....  -  ....   @             
         @=  .....  :=  .  +@  @  . .............. :# @:  ...  @  .....  @            
        @=  ...... :*     @*   @. =  ............  =   #@   ..  %  .....  @           
       @.........  *     @. ::  @ .@  ..........   @     @:   . :@  ..... .@          
      @:@ . ....  =-   =@ :     @= @:   .......  -@*      #@:    -@ .....  :@         
     @ @  ......  @  .@*         @. @@    ....  :=@         =@=  .@  .....  #         
    @:@: ....... +  =@             @.@*@:      -@@             %@::@  .....  @        
   @ =@   ...... =:@=     @@@@@@@   =@# *@@==:=@=  @@@@@@@@@@%   .*@= .  ... .@       
   -- @  : ..... @@    @@@@%%%-@@@            +    @@       @@@@    @ . =- .. .@      ███████╗██╗     ██╗██████╗ ██████╗ ███████╗██████╗            
  @ @@  :: ....  %   @@@% @:...@  @               @ %:::--:@  *@@@  @ . ::: .   @     ██╔════╝██║     ██║██╔══██╗██╔══██╗██╔════╝██╔══██╗           
  @. @  *  .... =+ @@@  @:. .:.:@                   @.+ ==.:*@  @@@ =.  :::..  @ @    █████╗  ██║     ██║██████╔╝██████╔╝█████╗  ██████╔╝           
  @- #  @  .... @=@@   @:.:+%+=::@                  @:..::*#=:@  -@@@.  =.: .  @% @   ██╔══╝  ██║     ██║██╔═══╝ ██╔═══╝ ██╔══╝  ██╔══██╗           
  @:@=  @  .... @@@   @:=*=*.-:.:%                  *. :*:  ..@    @@@  @ : .. -@ =   ██║     ███████╗██║██║     ██║     ███████╗██║  ██║           
  -:@  ..* ..   %@:   @ .   #*  :@                   +        @    @@=  @.  ..  @ @@  ╚═╝     ╚══════╝╚═╝╚═╝     ╚═╝     ╚══════╝╚═╝  ╚═╝           
   =@  : @    =@@@    @.      ..*                      .:.:::.%     @: @** . .  @ @@                                                                
    @  . @@.     @+    @.:::.:                                      %=- ** . =  @ @   ███████╗███████╗██████╗  ██████╗                              
    @:  .@ @     @    #                                  .:==####+- +:@  .   *  @@@   ╚══███╔╝██╔════╝██╔══██╗██╔═══██╗                             
     *   @ *@=:  @   :-=*#**+==:                  @      :==++=+*#= %@  @  : @ @        ███╔╝ █████╗  ██████╔╝██║   ██║                             
     @   .@  *@=  @ :*+=====-=:       *%%*#%%#**=           .::.     *@%: . = :@       ███╔╝  ██╔══╝  ██╔══██╗██║   ██║                             
     @    :@:  *@  @  -=-:::                                         @.:    @-@       ███████╗███████╗██║  ██║╚██████╔╝                             
      @=:  .=@@ @=@*@                                               @::.   @@         ╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝                              
       --%    -.=@  :                                              @#:. ..@@                                                                        
       @:-@    :::@                                              *@..  .#:            ███████╗ █████╗  ██████╗████████╗ ██████╗ ██████╗ ██╗   ██╗   
         % @:    ::@*                                          *@.-  .=@              ██╔════╝██╔══██╗██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗╚██╗ ██╔╝   
          @==@@    :=@@                                     *@-.:@@:@@                █████╗  ███████║██║        ██║   ██║   ██║██████╔╝ ╚████╔╝    
             @@@@@    .=@@                               @@= #@@@ @                   ██╔══╝  ██╔══██║██║        ██║   ██║   ██║██╔══██╗  ╚██╔╝     
                %@=@@@:::-=@@@*                      @@=:. -@@*                       ██║     ██║  ██║╚██████╗   ██║   ╚██████╔╝██║  ██║   ██║      
                    =@@  @@=-=@====@#  -      .==== @::@=@@@                          ╚═╝     ╚═╝  ╚═╝ ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝   ╚═╝      
                                 @@%@@ :-==+==-:::. @                                                                                               
                                      . ::::.:::::  . @                               ███████╗██╗      █████╗ ███████╗██╗  ██╗██╗███╗   ██╗ ██████╗ 
                                   #@@#::    .   -*%@ *                               ██╔════╝██║     ██╔══██╗██╔════╝██║  ██║██║████╗  ██║██╔════╝ 
                   @              @    :.@@@   @:     @@@@%                           █████╗  ██║     ███████║███████╗███████║██║██╔██╗ ██║██║  ███╗
                 @      @@@@@*=@   @        @:*      =@  @@=*@@@+      @              ██╔══╝  ██║     ██╔══██║╚════██║██╔══██║██║██║╚██╗██║██║   ██║
                @         @...:@    @*       @      @     @...@         =             ██║     ███████╗██║  ██║███████║██║  ██║██║██║ ╚████║╚██████╔╝
                          :            %          %       :    @        =             ╚═╝     ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝ 
"""

finish_banner = """
 ██████╗ ██╗  ██╗██╗
██╔═══██╗██║ ██╔╝██║
██║   ██║█████╔╝ ██║
██║   ██║██╔═██╗ ╚═╝
╚██████╔╝██║  ██╗██╗
 ╚═════╝ ╚═╝  ╚═╝╚═╝
"""

encrypted_key_iv = [
    [0x38, 0xB3, 0xEC, 0x3B, 0x3C, 0x5D, 0x34, 0x29, 0x8C, 0x38, 0x2E, 0xA8],
    [0xDF, 0x26, 0x9C, 0x42, 0xEE, 0x03, 0xEF, 0x0E, 0x49, 0x71, 0x1C, 0xDA],
    [0xD8, 0x96, 0x63, 0xF3, 0x27, 0x3B, 0xBF, 0xDF, 0x88, 0x64, 0x5B, 0xA6],
    [0x36, 0xFE, 0x95, 0x29, 0xEC, 0x19, 0xA2, 0x84, 0xDC, 0xAD, 0xC8, 0xDA],
    [0x19, 0x56, 0xA3, 0x53, 0xF2, 0xD5, 0x12, 0x01, 0x36, 0x1B, 0x09, 0x30],
    [0x2E, 0xAA, 0x02, 0x90, 0xC0, 0xDB, 0x42, 0x8B, 0x50, 0x14, 0x5D, 0x3B],
    [0xAF, 0x35, 0xCA, 0x82, 0x19, 0x9C, 0xC9, 0x99, 0x49, 0x4C, 0xA4, 0x4A],
    [0xD9, 0x81, 0xFF, 0xA0, 0xC1, 0x5F, 0x90, 0x2A, 0x65, 0x4B, 0xEF, 0x78],
    [0x02, 0xDF, 0xCA, 0xCD, 0xEC, 0xA0, 0xD6, 0xF9, 0xAE, 0xD8, 0x7E, 0x19],
    [0xD4, 0xFD, 0x39, 0xC6, 0x74, 0x0E, 0xC9, 0xD3, 0x09, 0x18, 0xAB, 0x76],
]


def aes128gcm_encrypt(key: bytes, iv: bytes, plaintext: bytes):
    cipher = AES.new(key, AES.MODE_GCM, iv)
    cipher.block_size = 128
    ciphertext = cipher.encrypt(plaintext)
    print(cipher.digest().hex().upper())
    return ciphertext


def generate_OTP(otp_config):
    logger.info("Trying to generate OTP")

    # Get the OTP config
    version = otp_config["version"]
    firmware = otp_config["firmware"]
    body = otp_config["body"]
    connect = otp_config["connect"]
    display = otp_config["display"]
    color = otp_config["color"]
    region = otp_config["region"]
    name = otp_config["name"]

    # Generate the OTP
    if (
        subprocess.run(
            [
                python_path,
                "scripts/otp.py",
                "generate",
                f"assets/OTP_{script_time}",
                f"--version={version}",
                f"--firmware={firmware}",
                f"--body={body}",
                f"--connect={connect}",
                f"--display={display}",
                f"--color={color}",
                f"--region={region}",
                f"--name={name}",
            ]
        ).returncode
        != 0
    ):
        logger.error("Failed to generate OTP")
        raise Exception("Generation failed")


def flash_OTP(otp_config):
    logger.info("Trying to flash OTP")

    # Get the OTP config
    version = otp_config["version"]
    firmware = otp_config["firmware"]
    body = otp_config["body"]
    connect = otp_config["connect"]
    display = otp_config["display"]
    color = otp_config["color"]
    region = otp_config["region"]
    name = otp_config["name"]

    # Flash the OTP
    if (
        subprocess.run(
            [
                python_path,
                "scripts/otp.py",
                "flash_all",
                f"--version={version}",
                f"--firmware={firmware}",
                f"--body={body}",
                f"--connect={connect}",
                f"--display={display}",
                f"--color={color}",
                f"--region={region}",
                f"--name={name}",
            ]
        ).returncode
        != 0
    ):
        logger.error("Failed to flash OTP")
        raise Exception("Flash failed")


def flash_core2_fus(fus_config):
    logger.info("Trying to flash Core2 FUS")

    # Get the FUS config
    fus_address = fus_config["address"]
    fus_file = (
        "assets/stm32wb5x_FUS_fw_for_fus_0_5_3.bin"
        if fus_config["from_version"] == "0.5.3"
        else "assets/stm32wb5x_FUS_fw.bin"
    )
    fus_statment = "AGREE_TO_LOSE_FLIPPER_FEATURES_THAT_USE_CRYPTO_ENCLAVE"

    # Flash the FUS
    if (
        subprocess.run(
            [
                python_path,
                "scripts/flash.py",
                "core2fus",
                f"--statement={fus_statment}",
                f"{fus_address}",
                f"{fus_file}",
            ]
        ).returncode
        != 0
    ):
        logger.error("Failed to flash Core2 FUS")
        raise Exception("Flash failed")


def flash_core2_radio(radio_config):
    logger.info("Trying to flash Core2 Radio")

    # Get the Radio config
    radio_address = radio_config["address"]
    radio_file = "assets/stm32wb5x_BLE_Stack_light_fw.bin"

    # Flash the Radio
    if (
        subprocess.run(
            [
                python_path,
                "scripts/flash.py",
                "core2radio",
                f"--addr={radio_address}",
                f"{radio_file}",
            ]
        ).returncode
        != 0
    ):
        logger.error("Failed to flash Core2 Radio")
        raise Exception("Flash failed")


def flash_bootloader():
    logger.info("Trying to flash Bootloader")

    bootloader = "assets/bootloader.bin"

    # Flash the bootloader
    if (
        subprocess.run(
            [
                python_path,
                "scripts/flash.py",
                "core1bootloader",
                bootloader,
            ]
        ).returncode
        != 0
    ):
        logger.error("Failed to flash Core1 bootloader")
        raise Exception("Flash failed")


def flash_firmware():
    logger.info("Trying to flash firmware")

    firmware = "assets/firmware.bin"

    # Flash the firmware
    if (
        subprocess.run(
            [
                python_path,
                "scripts/flash.py",
                "core1firmware",
                firmware,
            ]
        ).returncode
        != 0
    ):
        logger.error("Failed to flash Core1 firmware")
        raise Exception("Flash failed")


def flash_cks():
    logger.info("Trying to flash CKS")

    key_list = {
        "key_master.bin": "2",
        "key_1.bin": "3",
        "key_2.bin": "3",
        "key_3.bin": "3",
        "key_4.bin": "3",
        "key_5.bin": "3",
        "key_6.bin": "3",
        "key_7.bin": "3",
        "key_8.bin": "3",
        "key_9.bin": "3",
        "key_10.bin": "3",
    }

    for i in key_list.keys():
        if (
            subprocess.run(
                [
                    "STM32_Programmer_CLI",
                    "-c",
                    "port=SWD",
                    "freq=24000",
                    "-wusrkey",
                    f"assets/cks/{i}",
                    f"keytype={key_list[i]}",
                ]
            ).returncode
            != 0
        ):
            logger.error(f"Failed to flash CKS, {i}")
            raise Exception("Flash failed")


def generate_cks():
    logger.info("Trying to generate CKS")

    # gen the raw keys
    master_key: str = os.urandom(16).hex().upper()
    encrypted_keys_unencrypted: list[str] = [
        os.urandom(32).hex().upper() for _ in range(10)
    ]

    print(f"Master key:\n{master_key}\n")
    print(f"Encrypted keys (unencrypted):\n{encrypted_keys_unencrypted}\n")

    # encrypt the keys
    encrypted_keys = []
    for i in range(len(encrypted_keys_unencrypted)):
        encrypted_keys_unencrypted_bytes = bytes.fromhex(encrypted_keys_unencrypted[i])
        encrypted_iv = encrypted_key_iv[i]
        encrypted_key = aes128gcm_encrypt(
            bytes().fromhex(master_key),
            bytes(encrypted_iv + [0x00, 0x00, 0x00, 0x02]),
            encrypted_keys_unencrypted_bytes,
        )

        encrypted_keys.append(encrypted_key.hex().upper())
        with open("assets/cks/key_master.bin", "wb") as f:
            f.write(bytes().fromhex(master_key))

        with open(f"assets/cks/key_{i+1}.bin", "wb") as f:
            f.write(bytes([0x03]))  # Byte0: 0x03 (type=encrypted)
            f.write(bytes([0x20]))  # Byte1: 0x20 (size of the key: 32 bytes, 256 bits)
            f.write(encrypted_key)  # Byte2-Byte33: KeyData[0]-KeyData[31]
            f.write(bytes(encrypted_iv))  # Byte34-Byte45: IV[0]-IV[11]

    print(f"Encrypted keys:\n{encrypted_keys}\n")


def main():
    logger.info(banner)

    if config["OTP"]["generate_new"]:
        generate_OTP(config["OTP"])

    if config["CKS"]["generate_new"]:
        generate_cks()

    while True:
        logger.info("Starting")

        try:
            flash_OTP(config["OTP"])

            flash_core2_fus(config["FUS"])

            flash_core2_radio(config["radio"])

            if config["CKS"]["flash"]:
                flash_cks()

            flash_bootloader()

            flash_firmware()

            logger.info(finish_banner)
            if input("Press 'q' to exit, or any other key to continue: ") == "q":
                break
        except Exception:
            logger.error("Flash failed")
            if input("Press 'q' to exit, or any other key to continue: ") == "q":
                break


if __name__ == "__main__":
    main()
