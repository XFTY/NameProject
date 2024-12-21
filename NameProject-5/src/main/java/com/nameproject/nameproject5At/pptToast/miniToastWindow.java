package com.nameproject.nameproject5At.pptToast;

import com.nameproject.nameproject5At.NameProjectApplication;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Screen;
import javafx.stage.Stage;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.io.IOException;

public class miniToastWindow {
    private static Parent root2;
    private static final Logger logger = LogManager.getLogger(miniToastWindow.class);
    public static void sc() throws IOException {
        FXMLLoader fxmlLoader2 = new FXMLLoader(NameProjectApplication.class.getResource("fxml/miniWindow.fxml"));
        root2 = fxmlLoader2.load();
        logger.info("mini window FXML file loaded successfully");

        // 获取主屏幕
        Screen primaryScreen = Screen.getPrimary();
        logger.info("Primary screen retrieved successfully");

        // 获取屏幕的宽度和高度
        double screenWidth = primaryScreen.getBounds().getWidth();
        double screenHeight = primaryScreen.getBounds().getHeight();
        logger.info("Screen width: {}, height: {}", screenWidth, screenHeight);

        Scene scene2 = new Scene(root2, 400, 200);


        Stage miniStage = new Stage();
        miniStage.setScene(scene2);
    }

    public static void showMiniWindow(String resultName) {

    }
}
