    WARN SessionAuthenticator: ERROR: User: '{:urn=>"urn:publicid:IDN+domain+user+onelab.inria.r2lab.naoufal"}' does not exist
    WARN SessionAuthenticator: ERROR: User: '{:urn=>"urn:publicid:IDN+domain+user+onelab.inria.thierry.admin1"}' does not exist

This urn comes from the certificate and specifically here:

    $ openssl x509 -in user_cert.pem -noout -text
    <...>
    X509v3 extensions:
       X509v3 Subject Alternative Name:
             URI:uuid:7e21150c-d92b-451b-90ac-351b5bca63d6, URI:urn:publicid:IDN+domain+user+onelab.inria.thierry.admin1

===

    "urn": "urn:publicid:IDN+onelab:inria:thierry+slice+admin1",
    "urn": "urn:publicid:IDN+onelab:inria+user+thierry_parmentelat",
