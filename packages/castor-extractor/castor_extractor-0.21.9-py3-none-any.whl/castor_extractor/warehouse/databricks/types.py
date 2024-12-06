from typing import List, Optional, Tuple

Link = Tuple[str, str]
TablesColumns = Tuple[List[dict], List[dict]]
Ostr = Optional[str]
TimestampedLink = Tuple[str, str, Ostr]

OTimestampedLink = Optional[TimestampedLink]
