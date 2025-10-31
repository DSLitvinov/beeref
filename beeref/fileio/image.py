# This file is part of BeeRef.
#
# BeeRef is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# BeeRef is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with BeeRef.  If not, see <https://www.gnu.org/licenses/>.

import logging
import os.path
import tempfile
import socket
from urllib.error import URLError
from urllib import parse, request

from PyQt6 import QtGui

import exif
from lxml import etree
import plum


logger = logging.getLogger(__name__)

# Security settings
ALLOWED_SCHEMES = {'http', 'https'}
ALLOWED_DOMAINS = {'pinterest.com'}  # Whitelist of allowed domains
DEFAULT_TIMEOUT = 10  # seconds


def validate_url(url_string):
    """Validate URL for security concerns (SSRF protection).
    
    Returns:
        tuple: (is_valid: bool, parsed_url: ParseResult or None)
    """
    try:
        parsed = parse.urlparse(url_string)
        
        # Check scheme
        if parsed.scheme not in ALLOWED_SCHEMES:
            logger.warning(f'URL has disallowed scheme: {parsed.scheme}')
            return False, None
        
        # Check for localhost/internal IP addresses (SSRF protection)
        hostname = parsed.hostname
        if hostname:
            try:
                # Check for localhost variants
                if hostname in ('localhost', '127.0.0.1', '::1', '0.0.0.0'):
                    logger.warning(f'Blocked localhost URL: {hostname}')
                    return False, None
                
                # Check for private/internal IP ranges
                addr = socket.gethostbyname(hostname)
                if addr.startswith('10.') or addr.startswith('192.168.'):
                    logger.warning(f'Blocked private IP URL: {addr}')
                    return False, None
                if addr.startswith('172.') and 16 <= int(addr.split('.')[1]) <= 31:
                    logger.warning(f'Blocked private IP URL: {addr}')
                    return False, None
                    
            except socket.gaierror:
                logger.warning(f'Could not resolve hostname: {hostname}')
                return False, None
        
        return True, parsed
    except Exception as e:
        logger.warning(f'URL validation failed: {e}')
        return False, None


def exif_rotated_image(path=None):
    """Returns a QImage that is transformed according to the source's
    orientation EXIF data.
    """

    img = QtGui.QImage(path)
    if img.isNull():
        return img

    with open(path, 'rb') as f:
        try:
            exifimg = exif.Image(f)
        except (plum.exceptions.UnpackError, NotImplementedError):
            logger.exception(f'Exif parser failed on image: {path}')
            return img

    try:
        if 'orientation' in exifimg.list_all():
            orientation = exifimg.orientation
        else:
            return img
    except (NotImplementedError, ValueError):
        logger.exception(f'Exif failed reading orientation of image: {path}')
        return img

    transform = QtGui.QTransform()

    if orientation == exif.Orientation.TOP_RIGHT:
        return img.mirrored(horizontal=True, vertical=False)
    if orientation == exif.Orientation.BOTTOM_RIGHT:
        transform.rotate(180)
        return img.transformed(transform)
    if orientation == exif.Orientation.BOTTOM_LEFT:
        return img.mirrored(horizontal=False, vertical=True)
    if orientation == exif.Orientation.LEFT_TOP:
        transform.rotate(90)
        return img.transformed(transform).mirrored(
            horizontal=True, vertical=False)
    if orientation == exif.Orientation.RIGHT_TOP:
        transform.rotate(90)
        return img.transformed(transform)
    if orientation == exif.Orientation.RIGHT_BOTTOM:
        transform.rotate(270)
        return img.transformed(transform).mirrored(
            horizontal=True, vertical=False)
    if orientation == exif.Orientation.LEFT_BOTTOM:
        transform.rotate(270)
        return img.transformed(transform)

    return img


def load_image(path):
    if isinstance(path, str):
        path = os.path.normpath(path)
        return (exif_rotated_image(path), path)
    if path.isLocalFile():
        path = os.path.normpath(path.toLocalFile())
        return (exif_rotated_image(path), path)

    url = bytes(path.toEncoded()).decode()
    
    # Validate URL for security
    is_valid, parsed_url = validate_url(url)
    if not is_valid:
        logger.warning(f'URL validation failed for: {url}')
        img = exif_rotated_image()
        return (img, url)
    
    domain = '.'.join(parsed_url.netloc.split(".")[-2:])
    img = exif_rotated_image()
    if domain == 'pinterest.com':
        try:
            page_data = request.urlopen(url, timeout=DEFAULT_TIMEOUT).read()
            root = etree.HTML(page_data)
            url = root.xpath("//img")[0].get('src')
            # Re-validate the new URL
            is_valid, parsed_url = validate_url(url)
            if not is_valid:
                logger.warning(f'Pinterest extracted URL validation failed: {url}')
                return (img, url)
        except Exception as e:
            logger.debug(f'Pinterest image download failed: {e}')
            return (img, url)
    
    try:
        imgdata = request.urlopen(url, timeout=DEFAULT_TIMEOUT).read()
    except (URLError, socket.timeout) as e:
        logger.debug(f'Downloading image failed: {e}')
    else:
        with tempfile.TemporaryDirectory() as tmp:
            fname = os.path.join(tmp, 'img')
            with open(fname, 'wb') as f:
                f.write(imgdata)
                logger.debug(f'Temporarily saved in: {fname}')
            img = exif_rotated_image(fname)
    return (img, url)
