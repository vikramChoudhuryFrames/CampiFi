package com.hotspotchat.service;

import jakarta.servlet.http.HttpServletRequest;
import org.springframework.stereotype.Component;

import java.net.Inet4Address;
import java.net.InetAddress;
import java.net.NetworkInterface;
import java.util.Enumeration;

@Component
public class NetworkUtils {

    /**
     * Finds the local machine's active non-loopback IPv4 address
     * (e.g. Wi-Fi or Hotspot interface address like 10.5.4.19 or 192.168.43.10).
     */
    public String getHostLanIp() {
        try {
            Enumeration<NetworkInterface> interfaces = NetworkInterface.getNetworkInterfaces();
            while (interfaces.hasMoreElements()) {
                NetworkInterface iface = interfaces.nextElement();
                if (iface.isLoopback() || !iface.isUp()) continue;
                Enumeration<InetAddress> addresses = iface.getInetAddresses();
                while (addresses.hasMoreElements()) {
                    InetAddress addr = addresses.nextElement();
                    if (addr instanceof Inet4Address && !addr.isLoopbackAddress()) {
                        String hostAddress = addr.getHostAddress();
                        if (hostAddress != null && !hostAddress.startsWith("127.")) {
                            return hostAddress;
                        }
                    }
                }
            }
        } catch (Exception ignored) {}
        return "127.0.0.1";
    }

    /**
     * Returns true if the HTTP request was made from the server machine itself
     * (loopback or any of its own network interface addresses).
     */
    public boolean isHostDevice(HttpServletRequest request) {
        String remoteAddr = request.getRemoteAddr();
        if (remoteAddr == null) return false;

        // Loopback: browser opened via localhost or 127.0.0.1
        if ("127.0.0.1".equals(remoteAddr)
                || "0:0:0:0:0:0:0:1".equals(remoteAddr)
                || "::1".equals(remoteAddr)
                || "localhost".equalsIgnoreCase(remoteAddr)) {
            return true;
        }

        // Check all network interfaces of this machine
        try {
            Enumeration<NetworkInterface> ifaces = NetworkInterface.getNetworkInterfaces();
            while (ifaces.hasMoreElements()) {
                NetworkInterface iface = ifaces.nextElement();
                Enumeration<InetAddress> addrs = iface.getInetAddresses();
                while (addrs.hasMoreElements()) {
                    if (addrs.nextElement().getHostAddress().equalsIgnoreCase(remoteAddr)) {
                        return true;
                    }
                }
            }
        } catch (Exception ignored) {}

        return false;
    }

    /**
     * Extracts the real client IP address from the request,
     * handling proxies, tunnels (Cloudflare/ngrok), and forwarded headers.
     * If the client connects via localhost/loopback, it resolves to the machine's LAN IP.
     */
    public String getClientIp(HttpServletRequest request) {
        String ip = request.getHeader("CF-Connecting-IP"); // Cloudflare tunnel
        if (ip != null && !ip.isEmpty() && !"unknown".equalsIgnoreCase(ip)) {
            return ip.trim();
        }

        ip = request.getHeader("X-Forwarded-For");
        if (ip != null && !ip.isEmpty() && !"unknown".equalsIgnoreCase(ip)) {
            // X-Forwarded-For can contain multiple IPs; take the first client IP
            ip = ip.split(",")[0].trim();
        } else {
            ip = request.getHeader("X-Real-IP");
        }
        if (ip == null || ip.isEmpty() || "unknown".equalsIgnoreCase(ip)) {
            ip = request.getRemoteAddr();
        }
        // Handle loopback: when room is created or joined from localhost on host machine,
        // map it to the actual LAN IP of the machine on the Wi-Fi/Hotspot network.
        if ("0:0:0:0:0:0:0:1".equals(ip) || "::1".equals(ip) || "127.0.0.1".equals(ip) || "localhost".equalsIgnoreCase(ip)) {
            ip = getHostLanIp();
        }
        return ip;
    }

    /**
     * Extracts subnet based on network mode:
     * - "hotspot" (strict /24, e.g. 192.168.43.x)
     * - "campus" (broader match: /16 for 10.x.x.x or 172.16-31.x.x, or /24 for 192.168.x.x)
     * - "public" (matches public gateway IP)
     */
    public String extractNetworkIdentifier(String ip, String mode) {
        if (ip == null || ip.isBlank()) return "";
        if ("public".equalsIgnoreCase(mode)) {
            return ip; // Exact IP match (used when tunnel/public gateway is used)
        }

        String[] parts = ip.split("\\.");
        if (parts.length < 4) {
            return ip;
        }

        if ("campus".equalsIgnoreCase(mode)) {
            // Class A private (10.0.0.0/8) -> use first octet only
            // University campuses often span 10.1.x.x, 10.5.x.x, 10.6.x.x etc.
            if ("10".equals(parts[0])) {
                return parts[0]; // /8 — matches all 10.x.x.x
            }
            // Class B private (172.16.0.0 - 172.31.255.255)
            try {
                int secondOctet = Integer.parseInt(parts[1]);
                if ("172".equals(parts[0]) && secondOctet >= 16 && secondOctet <= 31) {
                    return parts[0] + "." + parts[1]; // /16
                }
            } catch (NumberFormatException ignored) {}

            // Otherwise standard /24
            return parts[0] + "." + parts[1] + "." + parts[2];
        }

        // Default "hotspot" mode: /24 (first 3 octets)
        return parts[0] + "." + parts[1] + "." + parts[2];
    }

    /**
     * Backward-compatible helper for /24
     */
    public String extractSubnet(String ip) {
        return extractNetworkIdentifier(ip, "hotspot");
    }

    public boolean isSameNetwork(String ip1, String ip2, String mode) {
        return extractNetworkIdentifier(ip1, mode).equals(extractNetworkIdentifier(ip2, mode));
    }
}
