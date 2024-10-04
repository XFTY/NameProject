package com.nameproject.nameproject5At.flusher;

import javafx.application.Platform;
import javafx.scene.control.Button;
import javafx.scene.control.Label;

import java.util.*;

public class Flush2v {

    private static volatile boolean stopFlushUi = false; // 控制是否停止刷新UI的标志
private static volatile boolean finalStopFlushUi = false; // 这个是针对while循环终止的标志
private int finalGet;

/**
 * 刷新UI的方法，用于动态更新界面中的标签和按钮状态。
 * @param nameList 姓名列表
 * @param labelController 标签控制器列表
 * @param btc 按钮控制器列表
 */
private void FlushUi(List<String> nameList, List<Label> labelController, List<Button> btc, Label welcomeTitle) {
    // 修改按钮状态
    Platform.runLater(() -> {
        btc.get(0).setDisable(true); // 禁用开始按钮
        btc.get(1).setDisable(false); // 启用停止按钮
        welcomeTitle.setText("正在滚动姓名...");
    });

    new Thread(() -> {
        // 打乱姓名列表
        Collections.shuffle(nameList);

        if (labelController.size() != 3) {
            System.err.println("Controller ERROR: " + labelController.size());
            return;
        }

        Random random = new Random();
        long stopTime = 500 + random.nextLong(501); // 设置随机停止时间
        System.out.println("StopTime = " + stopTime);

        long sleepTime = 100; // 初始睡眠时间

        while (true) {
            for (int i = 1; i < nameList.size() - 1; i++) {
                // 创建临时变量
                int finalI = i;

                if (stopFlushUi) {
                    btc.get(1).setDisable(true); // 禁用停止按钮
                    if (sleepTime >= stopTime) {
                        next_FlushUi(labelController, btc); // 循环结束，进入最终随机事件
                        stopFlushUi = false; // 重置刷新标志
                        finalStopFlushUi = true; // 设置循环终止标志
                        break;
                    }
                    sleepTime = sleepTime + 20; // 增加睡眠时间
                    System.out.println("SleepTime = " + sleepTime);
                }

                int counting = 0;

                // 更新控件文本
                Platform.runLater(() -> {
                    labelController.get(0).setText(nameList.get(finalI + 1)); // 更新左侧标签
                    labelController.get(1).setText(nameList.get(finalI)); // 更新中间标签
                    labelController.get(2).setText(nameList.get(finalI - 1)); // 更新右侧标签
                });

                try {
                    // 循环运行在多线程环境中，UI控件不会出现忙等待
                    Thread.sleep(sleepTime);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
            if (finalStopFlushUi) {
                finalStopFlushUi = false; // 重置循环终止标志
                btc.get(0).setDisable(false); // 可选：启用第一个按钮
                break; // 终止循环
            }
        }
    }).start(); // 启动新线程执行刷新逻辑
}


    private static void next_FlushUi(List<Label> labelController, List<Button> btc){

    }


    private void TestThread(Label clns) {
        new Thread(() -> {
            for (int i=0; i<=3; i++){
                int finalI = i;
                Platform.runLater(() -> {
                    clns.setText(String.valueOf(finalI));
                });
                try {
                    Thread.sleep(200);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }).start();
    }

    public void startFlush(List<Label> labelController, List<Button> buttonController, Label welcomeTitle) {
        // TestThread(labelController.get(0));

        List<String> testList = new ArrayList<>();

        Collections.addAll(testList, "1", "2", "3", "4", "5", "6", "7", "8", "9", "A");
        FlushUi(testList, labelController, buttonController, welcomeTitle);
    }

    public void stopFlush() {
        new Thread(() -> {
            stopFlushUi = true;
        }).start();
    }
}
