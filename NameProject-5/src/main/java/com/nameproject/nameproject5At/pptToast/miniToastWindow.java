package com.nameproject.nameproject5At.pptToast;

import com.nameproject.nameproject5At.IO.IOManager;
import com.nameproject.nameproject5At.NameProjectApplication;
import javafx.application.Platform;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.Label;
import javafx.stage.Screen;
import javafx.stage.Stage;
import javafx.stage.StageStyle;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.io.IOException;

public class miniToastWindow {
    private static Parent root2;
    private static Stage miniStage;
    private static double screenWidth;
    private static Scene scene2;
    // 设置窗口在屏幕右上方显示，并留出一些空隙
    private static final double offsetX = 20; // 空隙大小
    private static final double offsetY = 10; // 空隙大小
    private static final Logger logger = LogManager.getLogger(miniToastWindow.class);

    public static void sc() throws IOException {
        FXMLLoader fxmlLoader2 = new FXMLLoader(NameProjectApplication.class.getResource("fxml/miniWindow.fxml"));
        root2 = fxmlLoader2.load();
        logger.info("mini window FXML file loaded successfully");

        // 获取主屏幕
        Screen primaryScreen = Screen.getPrimary();
        logger.info("Primary screen retrieved successfully");

        // 获取屏幕的宽度和高度
        screenWidth = primaryScreen.getBounds().getWidth();
        double screenHeight = primaryScreen.getBounds().getHeight();
        logger.info("Screen width: {}, height: {}", screenWidth, screenHeight);

        scene2 = new Scene(root2, 400, 200);

        miniStage = new Stage();
        miniStage.setScene(scene2);
        miniStage.initStyle(StageStyle.UNDECORATED);
        miniStage.setAlwaysOnTop(true);

        // 设置窗口在屏幕右上方显示，并留出一些空隙
        miniStage.setX(screenWidth - scene2.getWidth() - offsetX);
        miniStage.setY(offsetY);

        // 初始位置在屏幕外
        miniStage.setY(-200);

        // miniStage.show();

    }

    public static void showMiniWindow(String resultName) {
        // 判断是否正在显示，如果正在显示，则忽略用户请求
        if (IOManager.ReturnIsMiniWindowShowing()) {
            logger.info("Mini window is already showing, ignoring user request.");
            return;
        } else {
            logger.info("Mini window is not showing, showing it.");
            IOManager.SetIsMiniWindowShowing(true);
        }

        if (miniStage == null) {
            try {
                sc();
            } catch (IOException e) {
                logger.error("Error initializing mini window", e);
                return;
            }
        }


        new Thread(() -> {
            Platform.runLater(() -> {
                Label label = (Label) root2.lookup("#resultNameLabel");

                label.setText(resultName);

                // 显示窗口
                miniStage.show();

//                TranslateTransition translateTransition = new TranslateTransition(Duration.seconds(2), root2);
//                translateTransition.setByY(10);
//                translateTransition.play();
            });

            while (miniStage.getY() <= 10) {
                miniStage.setY(miniStage.getY() + 1);
                try {
                    Thread.sleep(1);
                } catch (InterruptedException e) {
                    logger.error("Thread interrupted: ", e);
                }
            }

                try {
                    Thread.sleep(5000);
                } catch (InterruptedException e) {
                    logger.error("Thread interrupted: ", e);
                }

            Platform.runLater(() -> miniStage.hide());

            while (miniStage.getY() <= -100) {
                miniStage.setY(miniStage.getY() - 1);
                try {
                    Thread.sleep(1);
                } catch (InterruptedException e) {
                    logger.error("Thread interrupted: ", e);
                }
            }

            Platform.runLater(() -> {
                miniStage.setX(screenWidth - scene2.getWidth() - offsetX);
                miniStage.setY(offsetY);

                // 初始位置在屏幕外
                miniStage.setY(-200);

                IOManager.SetIsMiniWindowShowing(false);
            });

        }).start();
    }
}
