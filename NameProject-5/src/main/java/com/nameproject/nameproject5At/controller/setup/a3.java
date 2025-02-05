/* Copyright 2024-2025 XFTY, All Rights Reserved.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * For more information, see the LICENSE file in the root directory.
 */
package com.nameproject.nameproject5At.controller.setup;

import com.nameproject.nameproject5At.conf.NameWrapper;
import javafx.fxml.FXML;
import javafx.scene.control.Label;
import javafx.scene.control.TextArea;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
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
}
