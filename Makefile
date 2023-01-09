
subsystem:
	cd linux-stable && \
	$(MAKE) mrproper > /dev/zero && \
	$(MAKE) ARCH=${ARCHNAME} CROSS_COMPILE=aarch64-linux-gnu- tinyconfig > /dev/zero && \
	$(MAKE) clean > /dev/zero && \
	$(MAKE) ARCH=${ARCHNAME} CROSS_COMPILE=aarch64-linux-gnu- -n -k
