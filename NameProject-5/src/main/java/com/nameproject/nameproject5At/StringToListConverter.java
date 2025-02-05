/* Copyright 2024-2025 XFTY, All Rights Reserved.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * For more information, see the LICENSE file in the root directory.
 */
package com.nameproject.nameproject5At;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;


/**
 * @author XFTY
 * @author DeepSeek Ai
 * <p>
 * 这段代码是用于测试输入转换的示例代码，大部分为 DeepSeek 大模型生成，有我(XFTY)和 通义千问 大模型进行调试
 */
public class StringToListConverter {

    /**
     * 将输入字符串转换为List<Map<String, Object>>
     * @param input String
     * @return <code>result</code> - "List-Map-String, Object--"
     */
    public static List<Map<String, Object>> convert(String input) {
        List<Map<String, Object>> result = new ArrayList<>();
        String[] lines = input.split("\\n");
        for (String line : lines) {
            String[] parts = line.split("/", 2);
            Map<String, Object> entry = new HashMap<>();
            entry.put("name", parts[0].trim());

            Boolean sex = null;
            if (parts.length > 1) {
                String sexPart = parts[1].trim();
                if ("男".equals(sexPart)) sex = true;
                else if ("女".equals(sexPart)) sex = false;
            }
            entry.put("sex", sex);

            result.add(entry);
        }
        return result;
    }

    // 提取sex为null的条目
    public static List<Map<String, Object>> filterNullSexEntries(List<Map<String, Object>> list) {
        return list.stream()
                .filter(entry -> entry.get("sex") == null)
                .collect(Collectors.toList());
    }

    // 提取sex不为null的条目
    public static List<Map<String, Object>> filterNonNullSexEntries(List<Map<String, Object>> list) {
        return list.stream()
                .filter(entry -> entry.get("sex") != null)
                .collect(Collectors.toList());
    }

    public static void main(String[] args) {
        String input = "小明/男\n小红/女\n小蓝\n小黑/未知";

        // 原始转换结果
        List<Map<String, Object>> converted = convert(input);
        System.out.println("原始转换结果：");
        converted.forEach(System.out::println);

        // 提取sex为null的结果
        List<Map<String, Object>> nullSexList = filterNullSexEntries(converted);
        System.out.println("\n性别为null的条目：");
        nullSexList.forEach(System.out::println);

        // 提取sex非null的结果
        List<Map<String, Object>> nonNullSexList = filterNonNullSexEntries(converted);
        System.out.println("\n性别已填写的条目：");
        nonNullSexList.forEach(System.out::println);
    }
}