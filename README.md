### CPS2020 - Criptografia e Protocolos de Segurança
 
Given the [list of project](https://fenix.tecnico.ulisboa.pt/downloadFile/1689468335635574/ProjectList.pdf) this repository is a code application of the 15th item: __Ronald Cramer and Victor Shoup__ - [A Practical Public Key Cryptosystem Provably Secure against Adaptive Chosen Ciphertext](https://link.springer.com/content/pdf/10.1007/BFb0055717.pdf)

Developed by Pasquale Carnevale(97735) and Thamara Hessel(97872) 

https://bigprimes.org/

Run
python main.py 347 "some text"

python main.py 57719 "some text"

python main.py 81707 "some text"

### Abstract


### Introduction
The need to hide strategic messages from enemy eyes is as old as man's and with the passage of time a science was born that studies methods to "blur" this message, cryptogram, and make it invisible to people not authorized to read it. 
Cryptography has evolved a lot until today, and in this work we explore the use of asymmetric cryptography, which algorithms such as RSA and Rabin are the cornerstones of its. We explain how we managed to implement a CCA ecryption scheme based on DDH. We chose Python as the programming language for this project, as it allowed us to use some functions and libraries (one of them numpy) that made the work much faster and also intuitive. 
##### CCA Descriprion 

A chosen-ciphertext attack (CCA) is an attack model for cryptanalysis where the cryptanalyst can gather information by obtaining the decryptions of chosen ciphertexts. From these pieces of information the adversary can attempt to recover the hidden secret key used for decryption.[1] Chosen-ciphertext attacks, like other attacks, may be adaptive or non-adaptive. In an adaptive chosen-ciphertext attack, the attacker can use the results from prior decryptions to inform their choices of which ciphertexts to have decrypted. In a non-adaptive attack, the attacker chooses the ciphertexts to have decrypted without seeing any of the resulting plaintexts. After seeing the plaintexts, the attacker can no longer obtain the decryption of additional ciphertexts.

##### Method Approch

The whole structure has been designed so as to have a main part, which in our code is the main, in which are called each time of the subparts or special functions that allow the entire execution of the program.
The salient phases of our algorithm are surely those of key generation,ecrypting and decrypting.
```ruby
def main():
    m = sys.argv[2]
 ...
    p = int(sys.argv[1])
 ...
    G = subgroup(q, p)
    if len(G) < 255:
        print(len(G), "The subgroup must contain at least 255 to support ASCII")
 ...
    keys = keysGenerator(G,Zq,p)
    logTrace("Public and Private keys", keys, LOG)
    enc = encrypt(message, keys, G, Zq, p)
    print("Encrypted message", enc)
    dec = decrypt(enc,p,G,keys)
```
A peculiarity that can be immediately noticeable is the *<* 255, because if we want to encode our message in ASCII, a G group smaller than this number would not allow us to do it. 
##### Key Generator
The generation of the keys is quite simple and has some changes because we have chosen to implement a version without Hash function: there are the creation of more variables *y1,y2* because now we would have a vector d1 ...dk. 
##### Encryption
The *encrypt* function requires the incoming message, previously converted to ASCII, and by encoding it in G it passes it to the *chipertext* function which is the heart of the algorithm. 
It, like our [paper](https://link.springer.com/content/pdf/10.1007/BFb0055717.pdf) from which we refer, uses public and private keys to generate the hidden message. Letter by letter the *encription* is executed first, then the *chiper* function and finally this now encrypted letter is copied into a vector that will be finally printed our encrypted message.
Below are the code lines above the short description: 
```ruby
def encrypt(message, keys, G, Zq, p):
    encrypt = []
    for i in range(0, len(message)):
        logTrace("message", message[i], LOG)
        m = G[(message[i])]
        logTrace("m", m, LOG)
        cipher = cipherText(Zq, p, keys, m)
        logTrace("CipherText", cipher, LOG)
        encrypt.append(cipher)
    return encrypt
```
##### Decryption
The decryption happens very simply with the obvious output of the encryption, compared to the classic use that have proposed Cramer and Shoup, implementing the lite version we consider, we do not have the Hash function but through the verification of this relationship:  

![decrypt](file:///C:/Users/i_por/Desktop/Criptography/decryprion.png)
