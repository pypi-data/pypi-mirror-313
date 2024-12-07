-- Copyright (c) 2024, UChicago Argonne, LLC
-- BSD OPEN SOURCE LICENSE. Full license can be found in LICENSE.md
-- Comment line is the error message we will insert the error info in

-- Checks in this file are just cristal-specific consistency checks, and a network that fails these checks WILL CRASH the Cristal run

-- CRISTAL-RELATED NETWORK CHECKS;

-- There are no records in the county skims table for model run
SELECT count(*) == 0 FROM County_Skims;