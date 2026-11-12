package com.hotspotchat;

import com.hotspotchat.service.NetworkUtils;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class NetworkUtilsTest {

    private final NetworkUtils networkUtils = new NetworkUtils();

    @Test
    public void testCampusSubnetMatching_SameSecondOctet() {
        // Same building/AP block
        assertTrue(networkUtils.isSameNetwork("10.5.4.19", "10.5.130.14", "campus"));
    }

    @Test
    public void testCampusSubnetMatching_DifferentSecondOctets() {
        // Different buildings/APs across campus — must still match
        String laptopSubnet = networkUtils.extractNetworkIdentifier("10.5.4.19", "campus");
        String friend1Subnet = networkUtils.extractNetworkIdentifier("10.1.165.159", "campus");
        String friend2Subnet = networkUtils.extractNetworkIdentifier("10.6.164.37", "campus");

        assertEquals("10", laptopSubnet);
        assertEquals("10", friend1Subnet);
        assertEquals("10", friend2Subnet);

        assertTrue(networkUtils.isSameNetwork("10.5.4.19", "10.1.165.159", "campus"));
        assertTrue(networkUtils.isSameNetwork("10.5.4.19", "10.6.164.37", "campus"));
    }

    @Test
    public void testHotspotSubnetMatching() {
        assertTrue(networkUtils.isSameNetwork("192.168.43.10", "192.168.43.55", "hotspot"));
        assertFalse(networkUtils.isSameNetwork("192.168.43.10", "192.168.1.20", "hotspot"));
    }

    @Test
    public void testDifferentNetworkClasses_Campus() {
        // 10.x.x.x vs 192.168.x.x should NOT match
        assertFalse(networkUtils.isSameNetwork("10.5.4.19", "192.168.1.5", "campus"));
    }
}
