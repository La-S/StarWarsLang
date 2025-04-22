datapad character = incoming_comm();
datapad i = incoming_comm();

patrol _ within scan_range(i) {
    transmit(character);
}