package com.nameproject.nameproject5At.orginAWT;

import java.awt.*;

public class Toast4j {
    public static void _displayToast(String title, String main) throws AWTException {
        //Obtain only one instance of the SystemTray object
        SystemTray tray = SystemTray.getSystemTray();

        //If the icon is a file
        Image image = Toolkit.getDefaultToolkit().createImage("icon.png");
        //Alternative (if the icon is on the classpath):
        //Image image = Toolkit.getDefaultToolkit().createImage(getClass().getResource("icon.png"));

        TrayIcon trayIcon = new TrayIcon(image, "Tray Demo");
        //Let the system resize the image if needed
        trayIcon.setImageAutoSize(true);
        //Set tooltip text for the tray icon
        trayIcon.setToolTip("System tray icon demo");
        tray.add(trayIcon);

        trayIcon.displayMessage(title, main, TrayIcon.MessageType.INFO);
    }

    public static void displayToast(String title, String main) {
        try {
            if (SystemTray.isSupported()) {
                _displayToast(title, main);
            } else {
                System.err.println("System tray is not support!");
            }
        } catch (AWTException e) {
            System.err.println();
            e.printStackTrace();
        }
    }
}
