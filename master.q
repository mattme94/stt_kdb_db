\l db.q

// pub functions
.z.ws:{value -9!x}
pub:{neg[.z.w] -8! (x;eval(x,y)); 0N! (x;eval(x,y))}
pubp:{neg[.z.w] -8! x; 0N! x}
.z.pc: {delete from `subs where handle=x}

// Websocket Functions
loadPage:{pub '[`getNames`getSkills`getRarity;(("";"");("";);("";))]}
trimNames:{pub [`getNames;(x;y)]}
filterNames:{pub [`getMain;(x)]}

// get data methods
getMain:{w:$[all all null `$x;();enlist(in;`Name;enlist `$x)];
		pubp (`getMain;0!?[`master;w;`Name`Rarity!`Name`Rarity;`Traits`Skill!((?:;`Traits);(?:;`Skill))]);}
getRarity:{distinct (master`Rarity)}
getSkills:{distinct (master`Skill)}
getNames:{[rarity;skill] w:$[all all null `$rarity;();enlist(in;`Rarity;enlist `$rarity)];
	NameRarity:distinct ?[`master;w;();`Name];
	w:$[all all null `$skill;();enlist(in;`Skill;enlist `$skill)];
	NameSkill:distinct ?[`master;w;();`Name];
	NameSkill[where NameSkill in NameRarity]}