datapad word = incoming_comm();
datapad len_word = readout(word);
datapad reversed = "";
patrol i within scan_range(len_word) {
    datapad j = i + 1;
    datapad reversed = lightsaber(word, i, j) + reversed;
}
transmit(reversed);