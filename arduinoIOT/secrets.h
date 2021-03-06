#include <pgmspace.h>
 
#define SECRET
#define THINGNAME "ESP32"                         //change this
 
const char WIFI_SSID[] = "iPhone";               //change this
const char WIFI_PASSWORD[] = "12345678";           //change this
const char AWS_IOT_ENDPOINT[] = "a2ct0i272lnfu5-ats.iot.eu-west-1.amazonaws.com";       //change this
 
// Amazon Root CA 1
static const char AWS_CERT_CA[] PROGMEM = R"EOF(
-----BEGIN CERTIFICATE-----
MIIDQTCCAimgAwIBAgITBmyfz5m/jAo54vB4ikPmljZbyjANBgkqhkiG9w0BAQsF
ADA5MQswCQYDVQQGEwJVUzEPMA0GA1UEChMGQW1hem9uMRkwFwYDVQQDExBBbWF6
b24gUm9vdCBDQSAxMB4XDTE1MDUyNjAwMDAwMFoXDTM4MDExNzAwMDAwMFowOTEL
MAkGA1UEBhMCVVMxDzANBgNVBAoTBkFtYXpvbjEZMBcGA1UEAxMQQW1hem9uIFJv
b3QgQ0EgMTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBALJ4gHHKeNXj
ca9HgFB0fW7Y14h29Jlo91ghYPl0hAEvrAIthtOgQ3pOsqTQNroBvo3bSMgHFzZM
9O6II8c+6zf1tRn4SWiw3te5djgdYZ6k/oI2peVKVuRF4fn9tBb6dNqcmzU5L/qw
IFAGbHrQgLKm+a/sRxmPUDgH3KKHOVj4utWp+UhnMJbulHheb4mjUcAwhmahRWa6
VOujw5H5SNz/0egwLX0tdHA114gk957EWW67c4cX8jJGKLhD+rcdqsq08p8kDi1L
93FcXmn/6pUCyziKrlA4b9v7LWIbxcceVOF34GfID5yHI9Y/QCB/IIDEgEw+OyQm
jgSubJrIqg0CAwEAAaNCMEAwDwYDVR0TAQH/BAUwAwEB/zAOBgNVHQ8BAf8EBAMC
AYYwHQYDVR0OBBYEFIQYzIU07LwMlJQuCFmcx7IQTgoIMA0GCSqGSIb3DQEBCwUA
A4IBAQCY8jdaQZChGsV2USggNiMOruYou6r4lK5IpDB/G/wkjUu0yKGX9rbxenDI
U5PMCCjjmCXPI6T53iHTfIUJrU6adTrCC2qJeHZERxhlbI1Bjjt/msv0tadQ1wUs
N+gDS63pYaACbvXy8MWy7Vu33PqUXHeeE6V/Uq2V8viTO96LXFvKWlJbYK8U90vv
o/ufQJVtMVT8QtPHRh8jrdkPSHCa2XV4cdFyQzR1bldZwgJcJmApzyMZFo6IQ6XU
5MsI+yMRQ+hDKXJioaldXgjUkK642M4UwtBV8ob2xJNDd2ZhwLnoQdeXeGADbkpy
rqXRfboQnoZsG4q5WTP468SQvvG5
-----END CERTIFICATE-----
)EOF";
 
// Device Certificate                                               //change this
static const char AWS_CERT_CRT[] PROGMEM = R"KEY(
-----BEGIN CERTIFICATE-----
MIIDWjCCAkKgAwIBAgIVAPfZJJfPp7AaL5/40n8mkKcOv9JLMA0GCSqGSIb3DQEB
CwUAME0xSzBJBgNVBAsMQkFtYXpvbiBXZWIgU2VydmljZXMgTz1BbWF6b24uY29t
IEluYy4gTD1TZWF0dGxlIFNUPVdhc2hpbmd0b24gQz1VUzAeFw0yMjAyMTgxMTIz
MjFaFw00OTEyMzEyMzU5NTlaMB4xHDAaBgNVBAMME0FXUyBJb1QgQ2VydGlmaWNh
dGUwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDubSsFg0YoYEMVkCUX
6cvhwngihmPdSLFJ0qg5J8HVjM4Iv5FPYFxrJXY2RyaomIDbPivwc/vfCAQUIZ+L
a2oQmziNHkdjbzt0kNewHbVx60eWyL21N+jl23Q1vngNZDTsqw2XSJ4sl+CqsscV
GL6Da46fZBeHhV21lmjYob4YX8swL1cso7PKCwxNMWzVUwb9IQ8JQ92EFfK3B2vL
ZG7LTb6tXVGvj25BHpV+gHtO82c97FGfGgmZ9M3ZxXzYcWxSQZLTCCaTQrWDE9Xt
zSHpiynG9rqqGsafngKR4sn4uIOVNY9IY5sppxVkQwLl7ClEQ1aF2pPSPIDNuQia
lmKhAgMBAAGjYDBeMB8GA1UdIwQYMBaAFDJiF0EgH+dnsW/FUpK1zqiZkf71MB0G
A1UdDgQWBBS50BqRqL0EjOH2FNh6oJhQCIlf9DAMBgNVHRMBAf8EAjAAMA4GA1Ud
DwEB/wQEAwIHgDANBgkqhkiG9w0BAQsFAAOCAQEABuMpMqAuDLvKE3lkn3X03EpV
/KoY2dZkJiVj80RAcuAXHnszwgJJ1+M4duPUdXtW/arOzmu6M/r/nuZsd71XNd4D
8sUci99Stp1k6rj9E9dArUzjRZpgdy7km1gc3Gor4/dDj/h3tGHv9s+eFjUrilKA
ydqiIDpU56kA5rwG3s+08m1rklLdDbHw2OsYecSv9yiNQwdCmUkB4WKCMhq+bnYe
8dAI6YbBjGbthYl/ZsRejKBjG6UCEGttOGm4atCihhmcLZ8DaDoXue8f+sHwmsAS
VgQW9gtSxybep+b6M5cLYgZNTycGS2IokgXL7SiR0rktR9W+lIT+lPPLUKZuRw==
-----END CERTIFICATE-----
 
 
)KEY";
 
// Device Private Key                                               //change this
static const char AWS_CERT_PRIVATE[] PROGMEM = R"KEY(
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA7m0rBYNGKGBDFZAlF+nL4cJ4IoZj3UixSdKoOSfB1YzOCL+R
T2BcayV2NkcmqJiA2z4r8HP73wgEFCGfi2tqEJs4jR5HY287dJDXsB21cetHlsi9
tTfo5dt0Nb54DWQ07KsNl0ieLJfgqrLHFRi+g2uOn2QXh4VdtZZo2KG+GF/LMC9X
LKOzygsMTTFs1VMG/SEPCUPdhBXytwdry2Ruy02+rV1Rr49uQR6VfoB7TvNnPexR
nxoJmfTN2cV82HFsUkGS0wgmk0K1gxPV7c0h6Yspxva6qhrGn54CkeLJ+LiDlTWP
SGObKacVZEMC5ewpRENWhdqT0jyAzbkImpZioQIDAQABAoIBAQClLZZfhFmngUEY
gDtifMOVzR9jc81dsY25giqvJh8AbkMTBnyKDE0aoeJqqhJbPQQQX9sbA49cLXZ9
5+lbMnhRtuePxIlaluYO1IXI6lwY5xI6oSnkkS5ViBrTXPhY9rI/wCVzSIjkhffM
6nxH3lOmQm6VeEdgyQFp2yEZ67wBr41yyj0SEomVoFzgOdTCymtBmezH1Fg/uXjg
o1R4MuYseZH0XFOAM0WvYTnvlENY6kLOYPSPwIhUXRcpfVDU0ymieYlAY2WGnsYy
9pfrWZuBEacbyevWmA1lb0R7QjST2wz07WjCaNN2GkUsSCJ4n5rTSEz+qdA+F3oA
aT3lz/gBAoGBAPyTBIfe0aQBmK4foObMJ81ElvAd4gV/e1kMN9u7ongI1cLxX3kE
4FwCzoHWLngmYVCsXD+PdWdqTPFBu4kBwWvr7UT5FVUob6hBQnTNbS0dNJmrulro
2zZ3EMFyzqNP/cwUfzDmrffcGZiKJwLWrEd6c58V0lLLBsEDyH01n7HhAoGBAPGp
BsrhuTWk1b9Ub/HsSEekVg2/DWzjWxpYlb2LIoq28fwHJlkEI2XKGbFUpT23w/j8
aWQ5teufBdyuS+t+NbmJ1sW/IO9YhT+krVEgAV99XawDkkKZ+j03ArD6gRR/W19k
SBJ6iDXIfmXWrfOSZ17qjBUbxHyXuq3uwzocakjBAoGBAJp6BLRhGFE51Lryh0OB
q/pEsBhN/pYkQTnWWjefTCAkLzFa1Wy8Ccjcwpbwe11rA+wGbylEwaatgj+wV1XV
aApssqKTwXNjFt+OgmnT1qlYCnrOaFz/vEtUiT/3yuBhpTVzd9Nd0xscV99O58s5
pwbUovCytP+EQy479Rx3dqOhAoGAZyPP/Vk3lhijDcT4/lTtSH5wJ+/JyBaFNIpo
ZnxyoqeQQhO/HzDv9qq6KoBJAj1jS+pXBOrIpSa69sQBLSIxxd15p+56HQ032cDs
I/q3+0xjZV4k134mWmgXIvfXjasJkX4YcKKRbfsDT22/0nxC2DTc0smGI/MSPtfv
xOaJykECgYAsZMIlLXEnl1bGOyiJwY2DMRr/ajuCwh0u0yhM3znsNOdUez2ViNvq
SCWW/3+7fNmqYo3TSVMAz2CD+zQAx1+QLzKBTUyUTiTlYg0zywUuPBcY52Z+DRQS
KDDhgPO/pK7a4J1cy1fJLZmUwrSnHZrp9X7uG4NHPIc9+kwpTuqhUA==
-----END RSA PRIVATE KEY-----
 
 
)KEY";
