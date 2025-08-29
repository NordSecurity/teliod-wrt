include $(TOPDIR)/rules.mk

PKG_NAME:=nordvpn
PKG_VERSION:=1.0.0
PKG_RELEASE:=1

PKG_SOURCE_PROTO:=git
PKG_SOURCE_URL=https://github.com/NordSecurity/libtelio.git

# TODO: the PKG_SOURCE_VERSION always refers to the latest code which is good for testing but not so good for distributing. It should be tagged with the version
# we're happy to release
PKG_SOURCE_VERSION:=main
PKG_MIRROR_HASH:=skip

PKG_MAINTAINER:=Lukas Pukenis <lukas.pukenis@nordsecurity.com>
PKG_LICENSE:=GPLv3
PKG_BUILD_PARALLEL:=1

PKG_BUILD_DEPENDS:=rust/host

include $(INCLUDE_DIR)/package.mk
include ../../../packages/lang/rust/rust-package.mk

# +kmod-tun is required, however teliod has NepTUN built-in so +kmod-wireguard could, potentially, be optional
define Package/nordvpn
	SECTION:=net
	CATEGORY:=Network
	TITLE:=NordVPN
	DEPENDS:=$(RUST_ARCH_DEPENDS) +kmod-tun +kmod-wireguard
	URL:=https://www.nordsecurity.com
endef

define Package/nordvpn/description
	NordVPN is the gateway to a secure and private access to the internet.
endef

BINFILE := $(PKG_BUILD_DIR)/target/$(RUSTC_TARGET_ARCH)/release/teliod

define Build/Compile
	$(info RUSTC_TARGET_ARCH=$(RUSTC_TARGET_ARCH))	
	$(info PKG_BUILD_DIR=$(PKG_BUILD_DIR))
	$(info CARGO_PKG_VARS=$(CARGO_PKG_VARS))

	cd $(PKG_BUILD_DIR) && $(CARGO_PKG_VARS) BYPASS_LLT_SECRETS=1 cargo build -p teliod --release --target $(RUSTC_TARGET_ARCH)
	
	$(CURDIR)/../$(PKG_NAME)/version_placeholder_fix.py "$(BINFILE)" "$(PKG_VERSION)+openwrt"
endef

define Package/nordvpn/install
	$(INSTALL_DIR) $(1)/usr/sbin
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/target/$(RUSTC_TARGET_ARCH)/release/teliod $(1)/usr/sbin/nordvpn

	$(INSTALL_DIR) $(1)/etc/init.d
	$(INSTALL_BIN) ./files/nordvpn.init $(1)/etc/init.d/nordvpn
	$(INSTALL_DIR) $(1)/etc/config
	$(INSTALL_DATA) ./files/nordvpn.conf $(1)/etc/config/nordvpn
	$(INSTALL_DIR) $(1)/etc/nordvpn
	$(INSTALL_DATA) ./files/config.json $(1)/etc/nordvpn/config.json
endef

$(eval $(call RustBinPackage,nordvpn))
$(eval $(call BuildPackage,nordvpn))
