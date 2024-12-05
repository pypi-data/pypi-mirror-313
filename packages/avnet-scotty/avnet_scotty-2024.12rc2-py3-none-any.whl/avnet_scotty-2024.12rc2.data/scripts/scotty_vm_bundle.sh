#!/bin/bash
# SPDX-FileCopyrightText: (C) 2022 Avnet Embedded GmbH
# SPDX-License-Identifier: GPL-3.0-only

set -e

if [ $# -ne 5 ];
then
    echo "Usage ${0} vmname kernel disk_image appsimage outputname"
    exit 2
fi

VMNAME="$1"
KERNEL="$2"
DISK="$3"
APPSIMAGE="$4"
OUTPUTNAME="$5"
TMPDIR=$(mktemp -d)

KERNEL_PATH=$(realpath "${KERNEL}")
DISK_PATH=$(realpath "${DISK}")
KERNEL_FILENAME=$(basename "${KERNEL_PATH}")
DISK_FILENAME=$(basename "${DISK_PATH}")
APPSIMAGE_FILENAME=$(basename "${APPSIMAGE}")
SCRIPT_DIR=$(dirname "$(realpath "${0}")")

cp "${SCRIPT_DIR}/scotty_vm_create.sh.template" "${TMPDIR}/scotty_vm_create.sh"
sed -i "s/@@VMNAME@@/${VMNAME}/;s/@@KERNEL@@/${KERNEL_FILENAME}/;s/@@DISK@@/${DISK_FILENAME}/;s/@@APPSIMAGE@@/${APPSIMAGE_FILENAME}/" "${TMPDIR}/scotty_vm_create.sh"
chmod +x "${TMPDIR}/scotty_vm_create.sh"

tar -cjpf "${OUTPUTNAME}" "${KERNEL_PATH}" "${DISK_PATH}" "${APPSIMAGE}" "${TMPDIR}/scotty_vm_create.sh" --transform='s#.*/##'

rm -rf "${TMPDIR}"

