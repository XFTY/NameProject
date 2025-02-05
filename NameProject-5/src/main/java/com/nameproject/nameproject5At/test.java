package com.nameproject.nameproject5At;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class test {
    public static void main(String[] args) {
        List<Map<String, Object>> s = new ArrayList<>();

        // 使用 HashMap 来创建可变的 Map
        Map<String, Object> map1 = new HashMap<>();
        map1.put("name", "小明");
        map1.put("sex", true);
        s.add(map1);

        Map<String, Object> map2 = new HashMap<>();
        map2.put("name", "小红");
        map2.put("sex", false);
        s.add(map2);

        for (Map<String, Object> map : s) {
            System.out.println(map.get("name"));
            map.put("sex", null);  // 现在可以修改了
        }

        s.forEach(System.out::println);
    }
}
