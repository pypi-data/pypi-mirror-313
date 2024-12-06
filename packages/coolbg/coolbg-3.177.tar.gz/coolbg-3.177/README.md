#coolBG

Cả lyric và compilation đều tạo background trước
+ các component có duration <10s đều là intro, và được insert 1 lần
+ update ngoại trừ intro và outro vẫn giữ nguyên length
+ trong video có intro, thì thời gian của các layer(component) khác vẫn start_time từ 0, chứ không phải start_Time sau duration của intro.
