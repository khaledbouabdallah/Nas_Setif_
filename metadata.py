family_df['ن 00-20 سنة'] = family_df['ع 00-20 سنة']/family_df['ع الافراد']
family_df['ن 20-40 سنة'] = family_df['ع 20-40 سنة']/family_df['ع الافراد']
family_df['ن 40-60 سنة'] = family_df['ع 40-60 سنة']/family_df['ع الافراد']
family_df['ن 60-80 سنة'] = family_df['ع 60-80 سنة']/family_df['ع الافراد']
family_df['ن +80 سنة'] = family_df['ع +80 سنة']/family_df['ع الافراد']


family_df['ن 00-20 سنة'] = [round(x,2) for x in family_df['ن 00-20 سنة'] ]
family_df['ن 20-40 سنة'] = [round(x,2) for x in family_df['ن 20-40 سنة'] ]
family_df['ن 40-60 سنة'] = [round(x,2) for x in family_df['ن 40-60 سنة'] ]
family_df['ن 60-80 سنة'] = [round(x,2) for x in family_df['ن 60-80 سنة'] ]
family_df['ن +80 سنة'] = [round(x,2) for x in family_df['ن +80 سنة'] ]
