type color = RGB of (int * int * int)

let led_count = 500

let print_hex (i: int) = (
    if i < 0 || i > 255 then failwith "Invalid color value";
    let hx = ['0'; '1'; '2'; '3'; '4'; '5'; '6'; '7'; '8'; '9'; 'A'; 'B'; 'C'; 'D'; 'E'; 'F'] in
    i / 16 |> List.nth hx |> print_char;
    i mod 16 |> List.nth hx |> print_char
)

let print_frame (frame: color list) = (
    if List.length frame <> led_count then failwith "Invalid frame length";
    print_char '#';
    List.iter (function RGB (r, g, b) -> print_hex r; print_hex g; print_hex b) frame;
    print_endline ""
)



let rec loop duration = (
    let frame = List.init led_count (fun i -> RGB ((i + duration) mod 256, (i + duration)*i mod 256, (i + duration) / 2 mod 256)) in
    print_frame frame;
    if duration > 0 then (
        duration - 1 |> loop
    ) else ()
)

;;

print_string "#{\"version\":0, \"led_count\":500, \"fps\":60}\n";
loop 5400