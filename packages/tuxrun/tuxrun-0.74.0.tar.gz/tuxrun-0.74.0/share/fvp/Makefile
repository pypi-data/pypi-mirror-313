LAVA_IMAGE ?= ""
RUNTIME ?= "podman"

aemva_version ?= "11.24_11"
ifeq ($(shell uname -m),aarch64)
aemva_version_sha256 ?= "7a3593dafd3af6897b3a0a68f66701201f8f3e02a3d981ba47494b2f18853648"
aemva_arch = "Linux64_armv8l"
else
aemva_version_sha256 ?= "0f132334834cbc66889a62dd72057c976d7c7dfcfeec21799e9c78fb2ce24720"
aemva_arch = "Linux64"
endif
morello_version ?= "0.11_34"
morello_version_sha256 ?= "ed1e110fb7fa8732d4f1bea9af69491a9e3f7dbf57d2ce6ea916d3cdf910d324"

container_aemva_version = $(shell echo $(aemva_version)|sed -e 's|_|.|g')
container_morello_version = $(shell echo $(morello_version)|sed -e 's|_|.|g')

.PHONE: build

build: fvp-aemva fvp-morello

fvp-aemva: aemva/Dockerfile
	cd aemva && $(RUNTIME) build --build-arg version=$(aemva_version) --build-arg version_sha256=$(aemva_version_sha256) --build-arg arch=$(aemva_arch) --tag fvp:aemva-$(container_aemva_version) .

fvp-morello: morello/Dockerfile
	cd morello && $(RUNTIME) build --build-arg version=$(morello_version) --build-arg version_sha256=$(morello_version_sha256) --tag fvp:morello-$(container_morello_version) .

clean:
	$(RUNTIME) image rm fvp:aemva-$(container_aemva_version) fvp:morello-$(container_morello_version)
