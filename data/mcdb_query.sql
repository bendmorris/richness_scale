SELECT t.site_id, t.latitude, t.lonitude, s.genus, s.species, c.abundance
FROM MCDB_communities c
JOIN MCDB_species s
ON c.species_id = s.species_id
JOIN MCDB_sites t
ON c.site_id = t.site_id
