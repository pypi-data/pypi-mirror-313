from numba.typed import List
import numpy as np
from numba import njit

CACHE_JITTED = True

@njit(cache=CACHE_JITTED)
def djb2_hash(str_arr):
    hash_val = np.uint64(5381)
    for i in range(len(str_arr)):
        c = np.uint8(str_arr[i])
        if c == 0:
            break
        # Perform the hashing: hash * 33 + c
        hash_val = ((hash_val << np.uint64(5)) + hash_val) + c
    return hash_val

###################### SYMBOL ########################
@njit(cache=CACHE_JITTED)
def create_pkey_symbol_jit(records, count, pkey, start):
    n = np.uint32(pkey.size-1)
    for i in range(start, count):        
        h1 = djb2_hash(records['symbol'][i])
        h = np.uint32((h1) % n)
        if pkey[h] == -1:
            pkey[h] = i
        else:
            duplicatedkey = True
            j = 1
            while (                    
                    (records[pkey[h]]['symbol'] != records[i]['symbol'])
            ):
                h = np.uint32((h + j ** 2) % n)
                if pkey[h] == -1:
                    pkey[h] = i
                    duplicatedkey = False
                    break
                j += 1
            if duplicatedkey:
                return False        

    return True


@njit(cache=CACHE_JITTED)
def get_loc_symbol_jit(records, pkey, keys):
    n = np.uint32(pkey.size-1)
    loc = np.empty((keys.size, ))
    for i in range(keys.size):        
        h1 = djb2_hash(keys['symbol'][i])
        h = np.uint32((h1) % n)
        if pkey[h] == -1:
            loc[i] = pkey[h]
        else:
            j = 1
            while (                    
                    (records[pkey[h]]['symbol'] != keys[i]['symbol'])
            ):
                h = np.uint32((h + j ** 2) % n)
                if pkey[h] == -1:
                    break
                j += 1
            loc[i] = pkey[h]
    return loc


@njit(cache=CACHE_JITTED)
def upsert_symbol_jit(records, count, new_records, pkey, dateiniidx, dateendidx, dateunit,
                           portlastidx, portprevidx, symbollastidx, symbolprevidx):
    minchgid = count
    maxsize = records.size
    nrec = new_records.size
    n = np.uint32(pkey.size-1)

    for i in range(nrec):        
        h1 = djb2_hash(new_records['symbol'][i])
        h = np.uint32((h1) % n)
        found = False

        if pkey[h] != -1:  # hash already exists
            j = 1
            while True:  # check for collision & find a free bucket
                if (records[pkey[h]]['symbol'] == new_records[i]['symbol']):
                    # record exists update it
                    records[pkey[h]] = new_records[i]
                    minchgid = min(minchgid, pkey[h])
                    found = True
                    break
                # collision confirmed jump hash
                h = np.uint32((h + j ** 2) % n)
                if pkey[h] == -1:
                    break
                j += 1

        if not found:
            # Check space and append new record
            if count >= maxsize:
                break  # max size reached
            else:
                # append new record
                records[count] = new_records[i]                                
                pkey[h] = count                
                minchgid = min(minchgid, count)
                count += 1

    return count, minchgid


###################### DATE_SYMBOL ########################
@njit(cache=CACHE_JITTED)
def create_pkey_date_symbol_jit(records, count, pkey, dateiniidx, dateendidx, dateunit,
                                symbollastidx, symbolprevidx, start):
    n = np.uint32(pkey.size-1)
    for i in range(start, count):
        intdt = np.uint64(np.uint64(records['date'][i])/dateunit)
        if dateiniidx[intdt] == -1:
            dateiniidx[intdt] = i
        if dateendidx[intdt] < i:
            dateendidx[intdt] = i
        h0 = np.uint64(records['date'][i])
        h1 = djb2_hash(records['symbol'][i])
        h = np.uint32((h0 ^ h1) % n)
        
        if pkey[h] == -1:
            pkey[h] = i
        else:
            duplicatedkey = True
            j = 1
            while (
                    (records[pkey[h]]['date'] != records[i]['date']) |
                    (records[pkey[h]]['symbol'] != records[i]['symbol'])
            ):
                h = np.uint32((h + j ** 2) % n)
                if pkey[h] == -1:
                    pkey[h] = i
                    duplicatedkey = False
                    break
                j += 1
            if duplicatedkey:
                return False

        # update symbol index
        hs = np.uint32(h1 % n)
        if symbollastidx[hs] == -1:  # symbol not found
            symbollastidx[hs] = i
            symbolprevidx[i] = -1
        else:
            # check for collision
            found = True
            j = 1
            while (records[i]['symbol'] != records[symbollastidx[hs]]['symbol']):
                hs = np.uint32((hs + j**2) % n)
                if symbollastidx[hs] == -1:
                    symbollastidx[hs] = i
                    symbolprevidx[i] = -1
                    found = False
                    break
                j += 1

            if found:
                symbolprevidx[i] = symbollastidx[hs]
                symbollastidx[hs] = i

    return True


@njit(cache=CACHE_JITTED)
def get_loc_date_symbol_jit(records, pkey, keys):    
    n = np.uint32(pkey.size-1)
    loc = np.empty((keys.size, ),dtype=np.int64)
    for i in range(keys.size):
        h0 = np.uint64(keys['date'][i])
        h1 = djb2_hash(keys['symbol'][i])
        h = np.uint32((h0 ^ h1) % n)
        if pkey[h] == -1:
            loc[i] = pkey[h]
        else:
            j = 1
            while (
                    (records[pkey[h]]['date'] != keys[i]['date']) |
                    (records[pkey[h]]['symbol'] != keys[i]['symbol'])
            ):
                h = np.uint32((h + j**2) % n)
                if pkey[h] == -1:
                    break
                j += 1
            loc[i] = pkey[h]
    
    return loc


@njit(cache=CACHE_JITTED)
def upsert_date_symbol_jit(records, count, new_records, pkey, dateiniidx, dateendidx, dateunit,
                           portlastidx, portprevidx, symbollastidx, symbolprevidx):
    minchgid = count
    maxsize = records.size
    nrec = new_records.size
    n = np.uint32(pkey.size-1)

    for i in range(nrec):
        h0 = np.uint64(new_records['date'][i])
        h1 = djb2_hash(new_records['symbol'][i])
        h = np.uint32((h0 ^ h1) % n)
        found = False

        if pkey[h] != -1:  # hash already exists
            j = 1
            while True:  # check for collision & find a free bucket
                if (records[pkey[h]]['date'] == new_records[i]['date'] and
                   records[pkey[h]]['symbol'] == new_records[i]['symbol']):
                    # record exists update it
                    records[pkey[h]] = new_records[i]
                    minchgid = min(minchgid, pkey[h])
                    found = True
                    break
                # collision confirmed jump hash
                h = np.uint32((h + j ** 2) % n)
                if pkey[h] == -1:
                    break
                j += 1

        if not found:
            # Check space and append new record
            if count >= maxsize:
                break  # max size reached
            else:
                # append new record
                records[count] = new_records[i]
                intdt = np.uint64(np.uint64(new_records['date'][i]) / dateunit)
                if dateiniidx[intdt] == -1:
                    dateiniidx[intdt] = count
                if dateendidx[intdt] < count:
                    dateendidx[intdt] = count
                pkey[h] = count

                # update symbol index
                hs = np.uint32(h1 % n)
                if symbollastidx[hs] == -1:  # symbol not found
                    symbollastidx[hs] = count
                    symbolprevidx[count] = -1
                else:
                    # check for collision and find the appropriate bucket
                    found_symbol = True
                    j = 1
                    while records[symbollastidx[hs]]['symbol'] != new_records[i]['symbol']:
                        hs = np.uint32((hs + j ** 2) % n)
                        if symbollastidx[hs] == -1:
                            symbollastidx[hs] = count
                            symbolprevidx[count] = -1
                            found_symbol = False
                            break
                        j += 1

                    if found_symbol:
                        symbolprevidx[count] = symbollastidx[hs]
                        symbollastidx[hs] = count

                minchgid = min(minchgid, count)
                count += 1

    return count, minchgid

###################### DATE_TAG_SYMBOL ########################
@njit(cache=CACHE_JITTED)
def create_pkey_date_tag_symbol_jit(records, count, pkey, dateiniidx, dateendidx, dateunit,
                                          taglastidx, tagprevidx, symbollastidx, symbolprevidx, start):
    n = np.uint32(pkey.size-1)
    for i in range(start, count):
        intdt = np.uint64(np.uint64(records['date'][i])/dateunit)
        if dateiniidx[intdt] == -1:
            dateiniidx[intdt] = i
        if dateendidx[intdt] < i:
            dateendidx[intdt] = i
        h0 = np.uint64(records['date'][i])
        h1 = djb2_hash(records['tag'][i])
        h2 = djb2_hash(records['symbol'][i])
        h = np.uint32((h0 ^ h1 ^ h2) % n)
        
        if pkey[h] == -1:
            pkey[h] = i
        else:
            duplicatedkey = True
            j = 1
            while (
                    (records[pkey[h]]['date'] != records[i]['date']) |
                    (records[pkey[h]]['tag'] != records[i]['tag']) |
                    (records[pkey[h]]['symbol'] != records[i]['symbol'])
            ):
                h = np.uint32((h + j ** 2) % n)
                if pkey[h] == -1:
                    pkey[h] = i
                    duplicatedkey = False
                    break
                j += 1
            if duplicatedkey:
                return False

        # update tag index
        hs = np.uint32(h1 % n)
        if taglastidx[hs] == -1:  # tag not found
            taglastidx[hs] = i
            tagprevidx[i] = -1
        else:
            # check for collision
            found = True
            j = 1
            while (records[i]['tag'] != records[taglastidx[hs]]['tag']):
                hs = np.uint32((hs + j**2) % n)
                if taglastidx[hs] == -1:
                    taglastidx[hs] = i
                    tagprevidx[i] = -1
                    found = False
                    break
                j += 1

            if found:
                tagprevidx[i] = taglastidx[hs]
                taglastidx[hs] = i

        # update symbol index
        hs = np.uint32(h2 % n)
        if symbollastidx[hs] == -1:  # symbol not found
            symbollastidx[hs] = i
            symbolprevidx[i] = -1
        else:
            # check for collision
            found = True
            j = 1
            while (records[i]['symbol'] != records[symbollastidx[hs]]['symbol']):
                hs = np.uint32((hs + j**2) % n)
                if symbollastidx[hs] == -1:
                    symbollastidx[hs] = i
                    symbolprevidx[i] = -1
                    found = False
                    break
                j += 1

            if found:
                symbolprevidx[i] = symbollastidx[hs]
                symbollastidx[hs] = i

    return True


@njit(cache=CACHE_JITTED)
def get_loc_date_tag_symbol_jit(records, pkey, keys):
    n = np.uint32(pkey.size-1)
    loc = np.empty((keys.size, ))
    for i in range(keys.size):
        h0 = np.uint64(keys['date'][i])
        h1 = djb2_hash(keys['tag'][i])
        h2 = djb2_hash(keys['symbol'][i])
        h = np.uint32((h0 ^ h1 ^ h2) % n)
        if pkey[h] == -1:
            loc[i] = pkey[h]
        else:
            j = 1
            while (
                    (records[pkey[h]]['date'] != keys[i]['date']) |
                    (records[pkey[h]]['tag'] != keys[i]['tag']) |
                    (records[pkey[h]]['symbol'] != keys[i]['symbol'])
            ):
                h = np.uint32((h + j ** 2) % n)
                if pkey[h] == -1:
                    break
                j += 1
            loc[i] = pkey[h]
    return loc


@njit(cache=CACHE_JITTED)
def upsert_date_tag_symbol_jit(records, count, new_records, pkey, dateiniidx, dateendidx, dateunit,
                                     taglastidx, tagprevidx, symbollastidx, symbolprevidx):

    minchgid = count
    maxsize = records.size
    nrec = new_records.size
    n = np.uint32(pkey.size-1)

    for i in range(nrec):
        h0 = np.uint64(new_records['date'][i])
        h1 = djb2_hash(new_records['tag'][i])
        h2 = djb2_hash(new_records['symbol'][i])
        h = np.uint32((h0 ^ h1 ^ h2) % n)
        found = False

        if pkey[h] != -1:  # hash already exists
            j = 1
            while True:  # check for collision & find a free bucket
                if (records[pkey[h]]['date'] == new_records[i]['date'] and
                   records[pkey[h]]['tag'] == new_records[i]['tag'] and
                   records[pkey[h]]['symbol'] == new_records[i]['symbol']):
                    # record exists, update it
                    records[pkey[h]] = new_records[i]
                    minchgid = min(minchgid, pkey[h])
                    found = True
                    break
                # collision confirmed, jump hash
                h = np.uint32((h + j ** 2) % n)
                if pkey[h] == -1:
                    break
                j += 1

        if not found:
            # Check space and append new record
            if count >= maxsize:
                break  # max size reached
            else:
                # append new record
                records[count] = new_records[i]
                intdt = np.uint64(np.uint64(new_records['date'][i]) / dateunit)
                if dateiniidx[intdt] == -1:
                    dateiniidx[intdt] = count
                if dateendidx[intdt] < count:
                    dateendidx[intdt] = count
                pkey[h] = count

                # update tagfolio index
                hs = np.uint32(h1 % n)
                if taglastidx[hs] == -1:  # tagfolio not found
                    taglastidx[hs] = count
                    tagprevidx[count] = -1
                else:
                    # check for collision and find the appropriate bucket
                    found_tagfolio = True
                    j = 1
                    while records[taglastidx[hs]]['tag'] != new_records[i]['tag']:
                        hs = np.uint32((hs + j ** 2) % n)
                        if taglastidx[hs] == -1:
                            taglastidx[hs] = count
                            tagprevidx[count] = -1
                            found_tagfolio = False
                            break
                        j += 1

                    if found_tagfolio:
                        tagprevidx[count] = taglastidx[hs]
                        taglastidx[hs] = count

                # update symbol index
                hs = np.uint32(h2 % n)
                if symbollastidx[hs] == -1:  # symbol not found
                    symbollastidx[hs] = count
                    symbolprevidx[count] = -1
                else:
                    # check for collision and find the appropriate bucket
                    found_symbol = True
                    j = 1
                    while records[symbollastidx[hs]]['symbol'] != new_records[i]['symbol']:
                        hs = np.uint32((hs + j ** 2) % n)
                        if symbollastidx[hs] == -1:
                            symbollastidx[hs] = count
                            symbolprevidx[count] = -1
                            found_symbol = False
                            break
                        j += 1

                    if found_symbol:
                        symbolprevidx[count] = symbollastidx[hs]
                        symbollastidx[hs] = count

                minchgid = min(minchgid, count)
                count += 1

    return count, minchgid



###################### DATE_SYMBOL_SYMBOL1 ########################
@njit(cache=CACHE_JITTED)
def create_pkey_date_symbol_symbol1_jit(records, count, pkey, dateiniidx, dateendidx, dateunit,
                                        symbollastidx, symbolprevidx, start):
    n = np.uint32(pkey.size-1)
    for i in range(start, count):
        intdt = np.uint64(np.uint64(records['date'][i])/dateunit)
        if dateiniidx[intdt] == -1:
            dateiniidx[intdt] = i
        if dateendidx[intdt] < i:
            dateendidx[intdt] = i
        if records['symbol'][i] != records['symbol1'][i]:
            h0 = np.uint64(records['date'][i])
            h1 = djb2_hash(records['symbol'][i])
            h2 = djb2_hash(records['symbol1'][i])
            h = np.uint32((h0 ^ h1 ^ h2) % n)
        else:
            h0 = np.uint64(records['date'][i])
            h1 = djb2_hash(records['symbol'][i])
            h = np.uint32((h0 ^ h1) % n)
        if pkey[h] == -1:
            pkey[h] = i
        else:
            duplicatedkey = True
            j = 1
            while (
                    (records[pkey[h]]['date'] != records[i]['date']) |
                    (records[pkey[h]]['symbol'] != records[i]['symbol']) |
                    (records[pkey[h]]['symbol1'] != records[i]['symbol1'])
            ):
                h = np.uint32((h + j ** 2) % n)
                if pkey[h] == -1:
                    pkey[h] = i
                    duplicatedkey = False
                    break
                j += 1
            if duplicatedkey:
                return False

        # update symbol index
        hs = np.uint32(h1 % n)
        if symbollastidx[hs] == -1:  # symbol not found
            symbollastidx[hs] = i
            symbolprevidx[i] = -1
        else:
            # check for collision
            found = True
            j = 1
            while (records[i]['symbol'] != records[symbollastidx[hs]]['symbol']):
                hs = np.uint32((hs + j**2) % n)
                if symbollastidx[hs] == -1:
                    symbollastidx[hs] = i
                    symbolprevidx[i] = -1
                    found = False
                    break
                j += 1

            if found:
                symbolprevidx[i] = symbollastidx[hs]
                symbollastidx[hs] = i

    return True


@njit(cache=CACHE_JITTED)
def get_loc_date_symbol_symbol1_jit(records, pkey, keys):
    n = np.uint32(pkey.size-1)
    loc = np.empty((keys.size, ))
    for i in range(keys.size):
        if keys['symbol'][i] != keys['symbol1'][i]:
            h0 = np.uint64(keys['date'][i])
            h1 = djb2_hash(keys['symbol'][i])
            h2 = djb2_hash(keys['symbol1'][i])
            h = np.uint32((h0 ^ h1 ^ h2) % n)
        else:
            h0 = np.uint64(keys['date'][i])
            h1 = djb2_hash(keys['symbol'][i])
            h = np.uint32((h0 ^ h1) % n)
        if pkey[h] == -1:
            loc[i] = pkey[h]
        else:
            j = 1
            while (
                    (records[pkey[h]]['date'] != keys[i]['date']) |
                    (records[pkey[h]]['symbol'] != keys[i]['symbol']) |
                    (records[pkey[h]]['symbol1'] != keys[i]['symbol1'])
            ):
                h = np.uint32((h + j ** 2) % n)
                if pkey[h] == -1:
                    break
                j += 1
            loc[i] = pkey[h]
    return loc


@njit(cache=CACHE_JITTED)
def upsert_date_symbol_symbol1_jit(records, count, new_records, pkey, dateiniidx, dateendidx, dateunit,
                                   portlastidx, portprevidx, symbollastidx, symbolprevidx):
    minchgid = count
    maxsize = records.size
    nrec = new_records.size
    n = np.uint32(pkey.size-1)

    for i in range(nrec):
        if new_records['symbol'][i] != new_records['symbol1'][i]:
            h0 = np.uint64(new_records['date'][i])
            h1 = djb2_hash(new_records['symbol'][i])
            h2 = djb2_hash(new_records['symbol1'][i])
            h = np.uint32((h0 ^ h1 ^ h2) % n)
        else:
            h0 = np.uint64(new_records['date'][i])
            h1 = djb2_hash(new_records['symbol'][i])
            h = np.uint32((h0 ^ h1) % n)
        found = False

        if pkey[h] != -1:  # hash already exists
            j = 1
            while True:  # check for collision & find a free bucket
                if (records[pkey[h]]['date'] == new_records[i]['date'] and
                   records[pkey[h]]['symbol'] == new_records[i]['symbol'] and
                        records[pkey[h]]['symbol1'] == new_records[i]['symbol1']):
                    # record exists update it
                    records[pkey[h]] = new_records[i]
                    minchgid = min(minchgid, pkey[h])
                    found = True
                    break
                # collision confirmed jump hash
                h = np.uint32((h + j ** 2) % n)
                if pkey[h] == -1:
                    break
                j += 1

        if not found:
            # Check space and append new record
            if count >= maxsize:
                break  # max size reached
            else:
                # append new record
                records[count] = new_records[i]
                intdt = np.uint64(np.uint64(new_records['date'][i]) / dateunit)
                if dateiniidx[intdt] == -1:
                    dateiniidx[intdt] = count
                if dateendidx[intdt] < count:
                    dateendidx[intdt] = count
                pkey[h] = count

                # update symbol index
                hs = np.uint32(h1 % n)
                if symbollastidx[hs] == -1:  # symbol not found
                    symbollastidx[hs] = count
                    symbolprevidx[count] = -1
                else:
                    # check for collision and find the appropriate bucket
                    found_symbol = True
                    j = 1
                    while records[symbollastidx[hs]]['symbol'] != new_records[i]['symbol']:
                        hs = np.uint32((hs + j ** 2) % n)
                        if symbollastidx[hs] == -1:
                            symbollastidx[hs] = count
                            symbolprevidx[count] = -1
                            found_symbol = False
                            break
                        j += 1

                    if found_symbol:
                        symbolprevidx[count] = symbollastidx[hs]
                        symbollastidx[hs] = count

                minchgid = min(minchgid, count)
                count += 1

    return count, minchgid

###################### DATE_PORTFOLIO ########################
@njit(cache=CACHE_JITTED)
def create_pkey_date_portfolio_jit(records, count, pkey, dateiniidx, dateendidx, dateunit,
                                   portlastidx, portprevidx, start):
    n = np.uint32(pkey.size-1)
    for i in range(start, count):
        intdt = np.uint64(np.uint64(records['date'][i])/dateunit)
        if dateiniidx[intdt] == -1:
            dateiniidx[intdt] = i
        if dateendidx[intdt] < i:
            dateendidx[intdt] = i
        h0 = np.uint64(records['date'][i])
        h1 = djb2_hash(records['portfolio'][i])
        h = np.uint32((h0 ^ h1) % n)
        if pkey[h] == -1:
            pkey[h] = i
        else:
            duplicatedkey = True
            j = 1
            while (
                    (records[pkey[h]]['date'] != records[i]['date']) |
                    (records[pkey[h]]['portfolio'] != records[i]['portfolio'])
            ):
                h = np.uint32((h + j ** 2) % n)
                if pkey[h] == -1:
                    pkey[h] = i
                    duplicatedkey = False
                    break
                j += 1
            if duplicatedkey:
                return False

        # update port index
        hs = np.uint32(h1 % n)
        if portlastidx[hs] == -1:  # port not found
            portlastidx[hs] = i
            portprevidx[i] = -1
        else:
            # check for collision
            found = True
            j = 1
            while (records[i]['portfolio'] != records[portlastidx[hs]]['portfolio']):
                hs = np.uint32((hs + j**2) % n)
                if portlastidx[hs] == -1:
                    portlastidx[hs] = i
                    portprevidx[i] = -1
                    found = False
                    break
                j += 1

            if found:
                portprevidx[i] = portlastidx[hs]
                portlastidx[hs] = i

    return True


@njit(cache=CACHE_JITTED)
def get_loc_date_portfolio_jit(records, pkey, keys):
    n = np.uint32(pkey.size-1)
    loc = np.empty((keys.size, ))
    for i in range(keys.size):
        h0 = np.uint64(keys['date'][i])
        h1 = djb2_hash(keys['portfolio'][i])
        h = np.uint32((h0 ^ h1) % n)
        if pkey[h] == -1:
            loc[i] = pkey[h]
        else:
            j = 1
            while (
                    (records[pkey[h]]['date'] != keys[i]['date']) |
                    (records[pkey[h]]['portfolio'] != keys[i]['portfolio'])
            ):
                h = np.uint32((h + j ** 2) % n)
                if pkey[h] == -1:
                    break
                j += 1
            loc[i] = pkey[h]
    return loc


@njit(cache=CACHE_JITTED)
def upsert_date_portfolio_jit(records, count, new_records, pkey, dateiniidx, dateendidx, dateunit,
                              portlastidx, portprevidx, symbollastidx, symbolprevidx):
    minchgid = count
    maxsize = records.size
    nrec = new_records.size
    n = np.uint32(pkey.size-1)

    for i in range(nrec):
        h0 = np.uint64(new_records['date'][i])
        h1 = djb2_hash(new_records['portfolio'][i])
        h = np.uint32((h0 ^ h1) % n)
        found = False

        if pkey[h] != -1:  # hash already exists
            j = 1
            while True:  # check for collision & find a free bucket
                if (records[pkey[h]]['date'] == new_records[i]['date'] and
                   records[pkey[h]]['portfolio'] == new_records[i]['portfolio']):
                    # record exists update it
                    records[pkey[h]] = new_records[i]
                    minchgid = min(minchgid, pkey[h])
                    found = True
                    break
                # collision confirmed jump hash
                h = np.uint32((h + j ** 2) % n)
                if pkey[h] == -1:
                    break
                j += 1

        if not found:
            # Check space and append new record
            if count >= maxsize:
                break  # max size reached
            else:
                # append new record
                records[count] = new_records[i]
                intdt = np.uint64(np.uint64(new_records['date'][i]) / dateunit)
                if dateiniidx[intdt] == -1:
                    dateiniidx[intdt] = count
                if dateendidx[intdt] < count:
                    dateendidx[intdt] = count
                pkey[h] = count

                # update portfolio index
                hs = np.uint32(h1 % n)
                if portlastidx[hs] == -1:  # portfolio not found
                    portlastidx[hs] = count
                    portprevidx[count] = -1
                else:
                    # check for collision and find the appropriate bucket
                    found_portfolio = True
                    j = 1
                    while records[portlastidx[hs]]['portfolio'] != new_records[i]['portfolio']:
                        hs = np.uint32((hs + j ** 2) % n)
                        if portlastidx[hs] == -1:
                            portlastidx[hs] = count
                            portprevidx[count] = -1
                            found_portfolio = False
                            break
                        j += 1

                    if found_portfolio:
                        portprevidx[count] = portlastidx[hs]
                        portlastidx[hs] = count

                minchgid = min(minchgid, count)
                count += 1

    return count, minchgid

###################### DATE_PORTFOLIO_SYMBOL ########################
@njit(cache=CACHE_JITTED)
def create_pkey_date_portfolio_symbol_jit(records, count, pkey, dateiniidx, dateendidx, dateunit,
                                          portlastidx, portprevidx, symbollastidx, symbolprevidx, start):
    n = np.uint32(pkey.size-1)
    for i in range(start, count):
        intdt = np.uint64(np.uint64(records['date'][i])/dateunit)
        if dateiniidx[intdt] == -1:
            dateiniidx[intdt] = i
        if dateendidx[intdt] < i:
            dateendidx[intdt] = i
        h0 = np.uint64(records['date'][i])
        h1 = djb2_hash(records['portfolio'][i])
        h2 = djb2_hash(records['symbol'][i])
        h = np.uint32((h0 ^ h1 ^ h2) % n)
        if pkey[h] == -1:
            pkey[h] = i
        else:
            duplicatedkey = True
            j = 1
            while (
                    (records[pkey[h]]['date'] != records[i]['date']) |
                    (records[pkey[h]]['portfolio'] != records[i]['portfolio']) |
                    (records[pkey[h]]['symbol'] != records[i]['symbol'])
            ):
                h = np.uint32((h + j ** 2) % n)
                if pkey[h] == -1:
                    pkey[h] = i
                    duplicatedkey = False
                    break
                j += 1
            if duplicatedkey:
                return False

        # update port index
        hs = np.uint32(h1 % n)
        if portlastidx[hs] == -1:  # port not found
            portlastidx[hs] = i
            portprevidx[i] = -1
        else:
            # check for collision
            found = True
            j = 1
            while (records[i]['portfolio'] != records[portlastidx[hs]]['portfolio']):
                hs = np.uint32((hs + j**2) % n)
                if portlastidx[hs] == -1:
                    portlastidx[hs] = i
                    portprevidx[i] = -1
                    found = False
                    break
                j += 1

            if found:
                portprevidx[i] = portlastidx[hs]
                portlastidx[hs] = i

        # update symbol index
        hs = np.uint32(h2 % n)
        if symbollastidx[hs] == -1:  # symbol not found
            symbollastidx[hs] = i
            symbolprevidx[i] = -1
        else:
            # check for collision
            found = True
            j = 1
            while (records[i]['symbol'] != records[symbollastidx[hs]]['symbol']):
                hs = np.uint32((hs + j**2) % n)
                if symbollastidx[hs] == -1:
                    symbollastidx[hs] = i
                    symbolprevidx[i] = -1
                    found = False
                    break
                j += 1

            if found:
                symbolprevidx[i] = symbollastidx[hs]
                symbollastidx[hs] = i

    return True


@njit(cache=CACHE_JITTED)
def get_loc_date_portfolio_symbol_jit(records, pkey, keys):
    n = np.uint32(pkey.size-1)
    loc = np.empty((keys.size, ))
    for i in range(keys.size):
        h0 = np.uint64(keys['date'][i])
        h1 = djb2_hash(keys['portfolio'][i])
        h2 = djb2_hash(keys['symbol'][i])
        h = np.uint32((h0 ^ h1 ^ h2) % n)
        if pkey[h] == -1:
            loc[i] = pkey[h]
        else:
            j = 1
            while (
                    (records[pkey[h]]['date'] != keys[i]['date']) |
                    (records[pkey[h]]['portfolio'] != keys[i]['portfolio']) |
                    (records[pkey[h]]['symbol'] != keys[i]['symbol'])
            ):
                h = np.uint32((h + j ** 2) % n)
                if pkey[h] == -1:
                    break
                j += 1
            loc[i] = pkey[h]
    return loc


@njit(cache=CACHE_JITTED)
def upsert_date_portfolio_symbol_jit(records, count, new_records, pkey, dateiniidx, dateendidx, dateunit,
                                     portlastidx, portprevidx, symbollastidx, symbolprevidx):

    minchgid = count
    maxsize = records.size
    nrec = new_records.size
    n = np.uint32(pkey.size-1)

    for i in range(nrec):
        h0 = np.uint64(new_records['date'][i])
        h1 = djb2_hash(new_records['portfolio'][i])
        h2 = djb2_hash(new_records['symbol'][i])
        h = np.uint32((h0 ^ h1 ^ h2) % n)
        found = False

        if pkey[h] != -1:  # hash already exists
            j = 1
            while True:  # check for collision & find a free bucket
                if (records[pkey[h]]['date'] == new_records[i]['date'] and
                   records[pkey[h]]['portfolio'] == new_records[i]['portfolio'] and
                   records[pkey[h]]['symbol'] == new_records[i]['symbol']):
                    # record exists, update it
                    records[pkey[h]] = new_records[i]
                    minchgid = min(minchgid, pkey[h])
                    found = True
                    break
                # collision confirmed, jump hash
                h = np.uint32((h + j ** 2) % n)
                if pkey[h] == -1:
                    break
                j += 1

        if not found:
            # Check space and append new record
            if count >= maxsize:
                break  # max size reached
            else:
                # append new record
                records[count] = new_records[i]
                intdt = np.uint64(np.uint64(new_records['date'][i]) / dateunit)
                if dateiniidx[intdt] == -1:
                    dateiniidx[intdt] = count
                if dateendidx[intdt] < count:
                    dateendidx[intdt] = count
                pkey[h] = count

                # update portfolio index
                hs = np.uint32(h1 % n)
                if portlastidx[hs] == -1:  # portfolio not found
                    portlastidx[hs] = count
                    portprevidx[count] = -1
                else:
                    # check for collision and find the appropriate bucket
                    found_portfolio = True
                    j = 1
                    while records[portlastidx[hs]]['portfolio'] != new_records[i]['portfolio']:
                        hs = np.uint32((hs + j ** 2) % n)
                        if portlastidx[hs] == -1:
                            portlastidx[hs] = count
                            portprevidx[count] = -1
                            found_portfolio = False
                            break
                        j += 1

                    if found_portfolio:
                        portprevidx[count] = portlastidx[hs]
                        portlastidx[hs] = count

                # update symbol index
                hs = np.uint32(h2 % n)
                if symbollastidx[hs] == -1:  # symbol not found
                    symbollastidx[hs] = count
                    symbolprevidx[count] = -1
                else:
                    # check for collision and find the appropriate bucket
                    found_symbol = True
                    j = 1
                    while records[symbollastidx[hs]]['symbol'] != new_records[i]['symbol']:
                        hs = np.uint32((hs + j ** 2) % n)
                        if symbollastidx[hs] == -1:
                            symbollastidx[hs] = count
                            symbolprevidx[count] = -1
                            found_symbol = False
                            break
                        j += 1

                    if found_symbol:
                        symbolprevidx[count] = symbollastidx[hs]
                        symbollastidx[hs] = count

                minchgid = min(minchgid, count)
                count += 1

    return count, minchgid

###################### DATE_PORTFOLIO_SYMBOL_CLORDID ########################
@njit(cache=CACHE_JITTED)
def create_pkey_date_portfolio_symbol_clordid_jit(records, count, pkey, dateiniidx, dateendidx, dateunit,
                                                  portlastidx, portprevidx, symbollastidx, symbolprevidx, start):
    n = np.uint32(pkey.size-1)
    for i in range(start, count):
        intdt = np.uint64(np.uint64(records['date'][i])/dateunit)
        if dateiniidx[intdt] == -1:
            dateiniidx[intdt] = i
        if dateendidx[intdt] < i:
            dateendidx[intdt] = i
        h0 = np.uint64(records['date'][i])
        h1 = djb2_hash(records['portfolio'][i])
        h2 = djb2_hash(records['symbol'][i])
        h3 = djb2_hash(records['clordid'][i])
        h = np.uint32((h0 ^ h1 ^ h2 ^ h3) % n)
        
        if pkey[h] == -1:
            pkey[h] = i
        else:
            duplicatedkey = True
            j = 1
            while (
                    (records[pkey[h]]['date'] != records[i]['date']) |
                    (records[pkey[h]]['portfolio'] != records[i]['portfolio']) |
                    (records[pkey[h]]['symbol'] != records[i]['symbol']) |
                    (records[pkey[h]]['clordid'] != records[i]['clordid'])
            ):
                h = np.uint32((h + j ** 2) % n)
                if pkey[h] == -1:
                    pkey[h] = i
                    duplicatedkey = False
                    break
                j += 1
            if duplicatedkey:
                return False

        # update port index
        hs = np.uint32(h1 % n)
        if portlastidx[hs] == -1:  # port not found
            portlastidx[hs] = i
            portprevidx[i] = -1
        else:
            # check for collision
            found = True
            j = 1
            while (records[i]['portfolio'] != records[portlastidx[hs]]['portfolio']):
                hs = np.uint32((hs + j**2) % n)
                if portlastidx[hs] == -1:
                    portlastidx[hs] = i
                    portprevidx[i] = -1
                    found = False
                    break
                j += 1

            if found:
                portprevidx[i] = portlastidx[hs]
                portlastidx[hs] = i

        # update symbol index
        hs = np.uint32(h2 % n)
        if symbollastidx[hs] == -1:  # symbol not found
            symbollastidx[hs] = i
            symbolprevidx[i] = -1
        else:
            # check for collision
            found = True
            j = 1
            while (records[i]['symbol'] != records[symbollastidx[hs]]['symbol']):
                hs = np.uint32((hs + j**2) % n)
                if symbollastidx[hs] == -1:
                    symbollastidx[hs] = i
                    symbolprevidx[i] = -1
                    found = False
                    break
                j += 1

            if found:
                symbolprevidx[i] = symbollastidx[hs]
                symbollastidx[hs] = i

    return True


@njit(cache=CACHE_JITTED)
def get_loc_date_portfolio_symbol_clordid_jit(records, pkey, keys):
    n = np.uint32(pkey.size-1)
    loc = np.empty((keys.size, ))
    for i in range(keys.size):
        h0 = np.uint64(keys['date'][i])
        h1 = djb2_hash(keys['portfolio'][i])
        h2 = djb2_hash(keys['symbol'][i])
        h3 = djb2_hash(keys['clordid'][i])
        h = np.uint32((h0 ^ h1 ^ h2 ^ h3) % n)
        if pkey[h] == -1:
            loc[i] = pkey[h]
        else:
            j = 1
            while (
                    (records[pkey[h]]['date'] != keys[i]['date']) |
                    (records[pkey[h]]['portfolio'] != keys[i]['portfolio']) |
                    (records[pkey[h]]['symbol'] != keys[i]['symbol']) |
                    (records[pkey[h]]['clordid'] != keys[i]['clordid'])
            ):
                h = np.uint32((h + j ** 2) % n)
                if pkey[h] == -1:
                    break
                j += 1
            loc[i] = pkey[h]
    return loc


@njit(cache=CACHE_JITTED)
def upsert_date_portfolio_symbol_clordid_jit(records, count, new_records, pkey, dateiniidx, dateendidx, dateunit,
                                             portlastidx, portprevidx, symbollastidx, symbolprevidx):

    minchgid = count
    maxsize = records.size
    nrec = new_records.size
    n = np.uint32(pkey.size-1)

    for i in range(nrec):
        h0 = np.uint64(new_records['date'][i])
        h1 = djb2_hash(new_records['portfolio'][i])
        h2 = djb2_hash(new_records['symbol'][i])
        h3 = djb2_hash(new_records['clordid'][i])
        h = np.uint32((h0 ^ h1 ^ h2 ^ h3) % n)
        found = False

        if pkey[h] != -1:  # hash already exists
            j = 1
            while True:  # check for collision & find a free bucket
                if (records[pkey[h]]['date'] == new_records[i]['date'] and
                   records[pkey[h]]['portfolio'] == new_records[i]['portfolio'] and
                   records[pkey[h]]['symbol'] == new_records[i]['symbol'] and
                   records[pkey[h]]['clordid'] == new_records[i]['clordid']):
                    # record exists, update it
                    records[pkey[h]] = new_records[i]
                    minchgid = min(minchgid, pkey[h])
                    found = True
                    break
                # collision confirmed, jump hash using quadratic probing
                h = np.uint32((h + j ** 2) % n)
                if pkey[h] == -1:
                    break
                j += 1

        if not found:
            # Check space and append new record
            if count >= maxsize:
                break  # max size reached
            else:
                # append new record
                records[count] = new_records[i]
                intdt = np.uint64(np.uint64(new_records['date'][i]) / dateunit)
                if dateiniidx[intdt] == -1:
                    dateiniidx[intdt] = count
                if dateendidx[intdt] < count:
                    dateendidx[intdt] = count
                pkey[h] = count

                # update portfolio index
                hs = np.uint32(h1 % n)
                if portlastidx[hs] == -1:  # portfolio not found
                    portlastidx[hs] = count
                    portprevidx[count] = -1
                else:
                    # check for collision and find the appropriate bucket
                    found_portfolio = True
                    j = 1
                    while records[portlastidx[hs]]['portfolio'] != new_records[i]['portfolio']:
                        hs = np.uint32((hs + j ** 2) % n)
                        if portlastidx[hs] == -1:
                            portlastidx[hs] = count
                            portprevidx[count] = -1
                            found_portfolio = False
                            break
                        j += 1

                    if found_portfolio:
                        portprevidx[count] = portlastidx[hs]
                        portlastidx[hs] = count

                # update symbol index
                hs = np.uint32(h2 % n)
                if symbollastidx[hs] == -1:  # symbol not found
                    symbollastidx[hs] = count
                    symbolprevidx[count] = -1
                else:
                    # check for collision and find the appropriate bucket
                    found_symbol = True
                    j = 1
                    while records[symbollastidx[hs]]['symbol'] != new_records[i]['symbol']:
                        hs = np.uint32((hs + j ** 2) % n)
                        if symbollastidx[hs] == -1:
                            symbollastidx[hs] = count
                            symbolprevidx[count] = -1
                            found_symbol = False
                            break
                        j += 1

                    if found_symbol:
                        symbolprevidx[count] = symbollastidx[hs]
                        symbollastidx[hs] = count

                minchgid = min(minchgid, count)
                count += 1

    return count, minchgid

###################### DATE_PORTFOLIO_SYMBOL_TRADEID ########################
@njit(cache=CACHE_JITTED)
def create_pkey_date_portfolio_symbol_tradeid_jit(records, count, pkey, dateiniidx, dateendidx, dateunit,
                                                  portlastidx, portprevidx, symbollastidx, symbolprevidx, start):
    n = np.uint32(pkey.size-1)
    for i in range(start, count):
        intdt = np.uint64(np.uint64(records['date'][i])/dateunit)
        if dateiniidx[intdt] == -1:
            dateiniidx[intdt] = i
        if dateendidx[intdt] < i:
            dateendidx[intdt] = i
        h0 = np.uint64(records['date'][i])
        h1 = djb2_hash(records['portfolio'][i])
        h2 = djb2_hash(records['symbol'][i])
        h3 = djb2_hash(records['tradeid'][i])
        h = np.uint32((h0 ^ h1 ^ h2 ^ h3) % n)
        if pkey[h] == -1:
            pkey[h] = i
        else:
            duplicatedkey = True
            j = 1
            while (
                    (records[pkey[h]]['date'] != records[i]['date']) |
                    (records[pkey[h]]['portfolio'] != records[i]['portfolio']) |
                    (records[pkey[h]]['symbol'] != records[i]['symbol']) |
                    (records[pkey[h]]['tradeid'] != records[i]['tradeid'])
            ):
                h = np.uint32((h + j ** 2) % n)
                if pkey[h] == -1:
                    pkey[h] = i
                    duplicatedkey = False
                    break
                j += 1
            if duplicatedkey:
                return False

        # update port index
        hs = np.uint32(h1 % n)
        if portlastidx[hs] == -1:  # port not found
            portlastidx[hs] = i
            portprevidx[i] = -1
        else:
            # check for collision
            found = True
            j = 1
            while (records[i]['portfolio'] != records[portlastidx[hs]]['portfolio']):
                hs = np.uint32((hs + j**2) % n)
                if portlastidx[hs] == -1:
                    portlastidx[hs] = i
                    portprevidx[i] = -1
                    found = False
                    break
                j += 1

            if found:
                portprevidx[i] = portlastidx[hs]
                portlastidx[hs] = i

        # update symbol index
        hs = np.uint32(h2 % n)
        if symbollastidx[hs] == -1:  # symbol not found
            symbollastidx[hs] = i
            symbolprevidx[i] = -1
        else:
            # check for collision
            found = True
            j = 1
            while (records[i]['symbol'] != records[symbollastidx[hs]]['symbol']):
                hs = np.uint32((hs + j**2) % n)
                if symbollastidx[hs] == -1:
                    symbollastidx[hs] = i
                    symbolprevidx[i] = -1
                    found = False
                    break
                j += 1

            if found:
                symbolprevidx[i] = symbollastidx[hs]
                symbollastidx[hs] = i

    return True


@njit(cache=CACHE_JITTED)
def get_loc_date_portfolio_symbol_tradeid_jit(records, pkey, keys):
    n = np.uint32(pkey.size-1)
    loc = np.empty((keys.size, ))
    for i in range(keys.size):
        h0 = np.uint64(keys['date'][i])
        h1 = djb2_hash(keys['portfolio'][i])
        h2 = djb2_hash(keys['symbol'][i])
        h3 = djb2_hash(keys['tradeid'][i])
        h = np.uint32((h0 ^ h1 ^ h2 ^ h3) % n)
        if pkey[h] == -1:
            loc[i] = pkey[h]
        else:
            j = 1
            while (
                    (records[pkey[h]]['date'] != keys[i]['date']) |
                    (records[pkey[h]]['portfolio'] != keys[i]['portfolio']) |
                    (records[pkey[h]]['symbol'] != keys[i]['symbol']) |
                    (records[pkey[h]]['tradeid'] != keys[i]['tradeid'])
            ):
                h = np.uint32((h + j ** 2) % n)
                if pkey[h] == -1:
                    break
                j += 1
            loc[i] = pkey[h]
    return loc


@njit(cache=CACHE_JITTED)
def upsert_date_portfolio_symbol_tradeid_jit(records, count, new_records, pkey, dateiniidx, dateendidx, dateunit,
                                             portlastidx, portprevidx, symbollastidx, symbolprevidx):

    minchgid = count
    maxsize = records.size
    nrec = new_records.size
    n = np.uint32(pkey.size-1)

    for i in range(nrec):
        h0 = np.uint64(new_records['date'][i])
        h1 = djb2_hash(new_records['portfolio'][i])
        h2 = djb2_hash(new_records['symbol'][i])
        h3 = djb2_hash(new_records['tradeid'][i])
        h = np.uint32((h0 ^ h1 ^ h2 ^ h3) % n)
        found = False

        if pkey[h] != -1:  # hash already exists
            j = 1
            while True:  # check for collision & find a free bucket
                if (records[pkey[h]]['date'] == new_records[i]['date'] and
                   records[pkey[h]]['portfolio'] == new_records[i]['portfolio'] and
                   records[pkey[h]]['symbol'] == new_records[i]['symbol'] and
                   records[pkey[h]]['tradeid'] == new_records[i]['tradeid']):
                    # record exists, update it
                    records[pkey[h]] = new_records[i]
                    minchgid = min(minchgid, pkey[h])
                    found = True
                    break
                # collision confirmed, jump hash using quadratic probing
                h = np.uint32((h + j ** 2) % n)
                if pkey[h] == -1:
                    break
                j += 1

        if not found:
            # Check space and append new record
            if count >= maxsize:
                break  # max size reached
            else:
                # append new record
                records[count] = new_records[i]
                intdt = np.uint64(np.uint64(new_records['date'][i]) / dateunit)
                if dateiniidx[intdt] == -1:
                    dateiniidx[intdt] = count
                if dateendidx[intdt] < count:
                    dateendidx[intdt] = count
                pkey[h] = count

                # update portfolio index
                hs = np.uint32(h1 % n)
                if portlastidx[hs] == -1:  # portfolio not found
                    portlastidx[hs] = count
                    portprevidx[count] = -1
                else:
                    # check for collision and find the appropriate bucket
                    found_portfolio = True
                    j = 1
                    while records[portlastidx[hs]]['portfolio'] != new_records[i]['portfolio']:
                        hs = np.uint32((hs + j ** 2) % n)
                        if portlastidx[hs] == -1:
                            portlastidx[hs] = count
                            portprevidx[count] = -1
                            found_portfolio = False
                            break
                        j += 1

                    if found_portfolio:
                        portprevidx[count] = portlastidx[hs]
                        portlastidx[hs] = count

                # update symbol index
                hs = np.uint32(h2 % n)
                if symbollastidx[hs] == -1:  # symbol not found
                    symbollastidx[hs] = count
                    symbolprevidx[count] = -1
                else:
                    # check for collision and find the appropriate bucket
                    found_symbol = True
                    j = 1
                    while records[symbollastidx[hs]]['symbol'] != new_records[i]['symbol']:
                        hs = np.uint32((hs + j ** 2) % n)
                        if symbollastidx[hs] == -1:
                            symbollastidx[hs] = count
                            symbolprevidx[count] = -1
                            found_symbol = False
                            break
                        j += 1

                    if found_symbol:
                        symbolprevidx[count] = symbollastidx[hs]
                        symbollastidx[hs] = count

                minchgid = min(minchgid, count)
                count += 1

    return count, minchgid


####################### COMPOSITE INDEX ######################################
@njit(cache=CACHE_JITTED)
def get_date_portfolio_loc_jit(records, keys, pkey, portiniidx, portlist):
    n = np.uint32(pkey.size-1)
    loc = List()
    keyloc = List()
    for i in range(keys.size):
        h0 = np.uint64(keys['date'][i])
        h1 = djb2_hash(keys['portfolio'][i])
        h = np.uint32((h0 ^ h1) % n)
        if portiniidx[h] == -1:
            pass
        else:
            j = 1
            portfound = True
            recid = portlist[portiniidx[h]]
            while (
                    (records[recid]['date'] != keys[i]['date']) |
                    (records[recid]['portfolio'] != keys[i]['portfolio'])
            ):
                h = np.uint32((h + j ** 2) % n)
                if portiniidx[h] == -1:
                    portfound = False
                    break
                recid = portlist[portiniidx[h]]
                j += 1
            if portfound:
                curid = portiniidx[h]
                fid = portlist[curid]
                loc.append(fid)
                keyloc.append(i)
                nextid = portlist[curid+1]
                while nextid != -1:
                    curid = nextid
                    loc.append(portlist[curid])
                    keyloc.append(i)
                    nextid = portlist[curid+1]
    return loc, keyloc

@njit(cache=CACHE_JITTED)
def get_symbol_loc(records, symbollastidx, symbolprevidx, rec, maxids):
    n = np.uint32(symbollastidx.size - 1)
    symbol = rec[0]['symbol']
    symbolhash = djb2_hash(symbol)
    h = np.uint32(symbolhash % n)
    indexes = list()
    found = False

    # Find the initial position of the symbol in the hash table
    j = 1
    while symbollastidx[h] != -1:
        idx = symbollastidx[h]
        if records[idx]['symbol'] == symbol:
            indexes.append(idx)
            found = True
            break
        h = np.uint32((h + j ** 2) % n)
        j += 1

    if found:
        nids = 1
        # Backward traverse through the symbol indexes using symbolprevidx
        while symbolprevidx[idx] != -1:
            if (maxids != 0) & (nids >= maxids):
                break
            idx = symbolprevidx[idx]
            indexes.append(idx)
            nids += 1
            

    return indexes

@njit(cache=CACHE_JITTED)
def get_portfolio_loc(records, portlastidx, portprevidx, rec, maxids):
    n = np.uint32(portlastidx.size - 1)
    portfolio = rec[0]['portfolio']
    porthash = djb2_hash(portfolio)
    h = np.uint32(porthash % n)
    indexes = list()
    found = False

    # Find the initial position of the symbol in the hash table
    j = 1
    while portlastidx[h] != -1:
        idx = portlastidx[h]
        if records[idx]['portfolio'] == portfolio:
            indexes.append(idx)
            found = True
            break
        h = np.uint32((h + j ** 2) % n)
        j += 1

    if found:
        nids = 1
        # Backward traverse through the symbol indexes using portprevidx
        while portprevidx[idx] != -1:
            if (maxids != 0) & (nids >= maxids):
                break
            idx = portprevidx[idx]
            indexes.append(idx)
            nids += 1
            

    return indexes

@njit(cache=CACHE_JITTED)
def get_tag_loc(records, portlastidx, portprevidx, rec, maxids):    
    n = np.uint32(portlastidx.size - 1)
    tag = rec[0]['tag']
    taghash = djb2_hash(tag)
    h = np.uint32(taghash % n)
    indexes = list()
    found = False

    # Find the initial position of the symbol in the hash table
    j = 1
    while portlastidx[h] != -1:
        idx = portlastidx[h]
        if records[idx]['tag'] == tag:
            indexes.append(idx)
            found = True
            break
        h = np.uint32((h + j ** 2) % n)
        j += 1

    if found:
        nids = 1
        # Backward traverse through the symbol indexes using portprevidx
        while portprevidx[idx] != -1:
            if (maxids != 0) & (nids >= maxids):
                break
            idx = portprevidx[idx]
            indexes.append(idx)
            nids += 1
            

    return indexes
