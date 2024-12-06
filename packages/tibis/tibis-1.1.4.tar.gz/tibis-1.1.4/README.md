# Tibis

![image](https://user-images.githubusercontent.com/5250807/166554591-47e85ac2-2f59-4e33-ba95-a76f2ea41818.png)


Tibis (Thot the IBIS) is a tool to help manage encrypted directories (named data container here) 

Name is inspired by the Egyptian god of writers and protector of knowledge 

## TLDR; Setup 

```
pip install tibis
```

## TLDR; Usage 

### Customise the data location path

Default config is set to be at : 
```
~/.config/tibis/config.yml
```
You HAVE TO edit the storage_path to something more secure than /tmp :) 

### Create a new data container
```
tibis create <name>
```
Thot will ask you a passphrase, choose a good one !

### List data containers
```
tibis list 
```

### Mount a data container 
```
tibis unlock <name> <destination path>
```
Thot will ask your passphrase.

### Lock a data container
```
tibis lock <name>
```
Thot will not ask your passphrase.. because it's PGP Public key.

### Remove an entry 
```
tibis delete <name>
```
Thot will ask you a confirmation, take care !
## Why ? 
Because we have to handle with sensitive files, and store them securly can be boring

## How ? 
Tibis is a kind of python wrapper on pgp keys and gzip files. 

Yes, nothing more. 

## Why do we have to set passphrase ? 
Security is a matter of trust, if you don't trust your laptop enough to store sensitive data, why leave the keys in it ?

By using a passphrase, access to the data needs : something you have ( data / key ) and something you know ( passphrase ) 

## What does chat-gpt think about it ? 



```
Q: 
do you think storing gpg encrypted tar files is a good idea ? 

A: 
Storing GPG-encrypted tar files can be a good idea for protecting sensitive data, as long as you follow best practices for encryption and key management.

Encrypting data with GPG (GNU Privacy Guard) provides strong encryption and can help to prevent unauthorized access to your data, even if it is stolen or intercepted. GPG uses public-key cryptography, which means that you can encrypt data with a public key and only the holder of the corresponding private key can decrypt it.

Using tar (tape archive) to bundle files together before encryption can simplify the process of managing and transferring encrypted data, especially if you have many files that you want to encrypt as a single unit. Tar files can also be compressed, which can save disk space and bandwidth during transmission.

However, there are some important considerations to keep in mind when using GPG-encrypted tar files:

Key management: You need to securely manage your GPG keys, as they are critical to the security of your encrypted data. Make sure to create strong, unique passwords for your private keys and store them in a secure location.

Verification: Before decrypting a GPG-encrypted tar file, make sure to verify the integrity of the file and the identity of the sender. This can help prevent against attacks such as man-in-the-middle or tampering.

Storage location: Make sure to store your encrypted tar files in a secure location, such as an encrypted hard drive or cloud storage with strong encryption and access controls.

Password management: If you use a password to protect the contents of the tar file, make sure to use a strong, unique password and do not reuse it for other purposes.
```
