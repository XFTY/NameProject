/* Copyright 2024-2025 XFTY, All Rights Reserved.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * For more information, see the LICENSE file in the root directory.
 */
package com.nameproject.nameproject5At.controller.setup;

import com.nameproject.nameproject5At.conf.NameWrapper;
import com.nameproject.nameproject5At.controller.StringToListConverter;
import com.nameproject.nameproject5At.guessGender.GenderGuesser;
import javafx.application.Platform;
import javafx.fxml.FXML;
import javafx.scene.control.Label;
import javafx.scene.control.TextArea;
import javafx.scene.paint.Color;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.logging.Logger;

public class a3 {
    private final Logger logger = Logger.getLogger(a3.class.getName());
    @FXML
    private TextArea nameList;

    @FXML
    private Label noticeLabel;

    @FXML
    protected void onCheckButtonClicked() {
        noticeLabel.setText("正在检查");
        logger.info("Check button clicked");
        logger.info("checking");

        NameWrapper nameWrapper = new NameWrapper();

        try {
            String[] nameListArray = nameList.getText().split("\n");
            /* 此时，nameListArray 的数据内容如下：
            * ["小明/男", "小红/女", "小芳/女"]
            * 需要对数据进行进一步处理
             */

            // 创建结果列表，保证数据存储的顺序与输入的顺序一致
            // 有性别的数据
            List<Map<Map<String, String>, Map<String, Integer>>> haveSexResult = new ArrayList<>();
            // 无性别的数据
            List<Map<Map<String, String>, Map<String, Integer>>> haveNoSexResult = new ArrayList<>();
            // 该变量用于存储下面的遍历结果
            Map<Map<String, String>, Map<String, Integer>> rlmap;

            for (String name : nameListArray) {
                rlmap = nameWrapper.splitSex(name);

            }

        } catch (Exception e) {
            noticeLabel.setText("格式错误");
        }
    }

    @FXML
    protected void onGenderGuessButtonClicked() {
        this.noticeLabel.setText("处理中......");
        String nameListStringLabel = this.nameList.getText();

        // 处理null条目
        new Thread(() -> {
            Platform.runLater(() -> this.noticeLabel.setText("数据打包中......"));
            // 获取原始转换结果
            final List<Map<String, Object>> converted = StringToListConverter.convert(nameListStringLabel);
            //logger.info("converted value is:");
            //converted.forEach(System.out::println);

            // 提取null条目
            List<Map<String, Object>> nullSexList = StringToListConverter.filterNullSexEntries(converted);
            // 提取非null项目
            List<Map<String, Object>> nonNullSexList = StringToListConverter.filterNonNullSexEntries(converted);

            Platform.runLater(() -> this.noticeLabel.setText("计算中......"));

            // 处理数据
            for (Map<String, Object> s: nullSexList) {
                // System.out.println(s.get("name"));
                GenderGuesser.GuessResult guessResult = GenderGuesser.guess((String) s.get("name"));
                // System.out.println(guessResult.getGender());
                s.put("sex", guessResult.getGender());
                try {
                    Thread.sleep(100);
                } catch (Exception e) {

                }
            }

            nullSexList.addAll(nonNullSexList);

            // nullSexList.forEach(System.out::println);

            StringBuilder finallyResult = new StringBuilder();
            Platform.runLater(() -> this.noticeLabel.setText("渲染中......"));

            // 渲染结果
            for (Map<String, Object> stringObjectMap : nullSexList) {
                finallyResult.append(stringObjectMap.get("name"));
                finallyResult.append("/");
                if (Objects.equals(String.valueOf(stringObjectMap.get("sex")), "true")) {
                    finallyResult.append("男");
                } else if (!Objects.equals(String.valueOf(stringObjectMap.get("sex")), "true")) {
                    finallyResult.append("女");
                }
                finallyResult.append("\n");
            }

            // 输出结果
            nameList.setText(finallyResult.toString());

            Platform.runLater(() -> {
                this.noticeLabel.setTextFill(Color.GREEN);
                this.noticeLabel.setText("成功！您可以修改预测不符的性别，然后，请点击“检查输入”。");
            });

        }).start();

    }


}
