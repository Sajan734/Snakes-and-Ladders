    dice = get_dice_value()
    old_value = player_entry[2]
    player_entry[2] += dice
    
    transport_piece(player_entry, old_value)