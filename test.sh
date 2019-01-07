# Script for the pull of all the nutanixworkshop github repositories

# Get the list of the repositories and clone them:
for map in `curl https://github.com/nutanixworkshops | grep "type=\"repository\"" | cut -d "=" -f 5 | cut -d"/" -f 3 | rev | cut -c3- | rev`; do cd github; git clone https://github.com/nutanixworkshops/$map ; done

# What is written in the README.md file in all the cloned repositories?
for map in `ls  ~/github`; do echo $map; cat visual$map/README.md; done