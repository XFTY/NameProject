/* Copyright 2024-2025 XFTY, All Rights Reserved.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * For more information, see the LICENSE file in the root directory.
 */
package com.nameproject.nameproject5At.conf;

import com.nameproject.nameproject5At.NameProjectApplication;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.yaml.snakeyaml.Yaml;

import java.io.InputStream;
import java.util.Map;

public class ConfManager {
    private static final Logger logger = LogManager.getLogger(ConfManager.class);

    // 读取&存储 软件配置 文件
    private static final Map<String, Object> sysinfo = GetSysInfo();
    // 读取&存储 用户配置 文件
    private static final Map<String, Object> usrinfo = GetUsrInfo();

    private static Map<String, Object> GetSysInfo() {
        return loadSysInfo();
    }

    private static Map<String, Object> GetUsrInfo() {
        return loadUsrInfo();
    }

    private static Map<String, Object> loadSysInfo() {
        try (InputStream inputStream = NameProjectApplication.class.getResourceAsStream("/com/nameproject/nameproject5At/config/SoftwareInfo.yaml")) {
            if (inputStream == null) {
                logger.error("无法找到软件配置文件: /config/SoftwareInfo.yaml");
                return null;
            }
            Yaml yaml = new Yaml();
            return yaml.load(inputStream);
        } catch (Exception e) {
            logger.error("读取软件配置文件时发生错误", e);
            return null;
        }
    }

    private static Map<String, Object> loadUsrInfo() {
        try {
            ConfigCreator configCreator = new ConfigCreator();
            return configCreator.getOrCreateConfigFile();
        } catch (Exception e) {
            logger.error("读取用户配置文件时发生错误", e);
            return null;
        }
    }

    public static Map<String, Object> ReturnSysInfo() {
        return sysinfo;
    }

    public static Map<String, Object> ReturnUsrInfo() {
        return usrinfo;
    }
}
