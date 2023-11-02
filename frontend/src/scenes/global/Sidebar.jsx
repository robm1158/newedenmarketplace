import 'react-pro-sidebar/dist/css/styles.css';
import React from 'react';
import { ProSidebar, Menu, MenuItem, SubMenu } from 'react-pro-sidebar';
import marketGroupsJSON from '../../constants/marketGroups.json';
import { ItemEnum } from '../../constants/ItemEnum';

const CustomSidebar = ({ handleSidebarClick }) => {

    const REVERSED_ITEM_ENUM = Object.keys(ItemEnum).reduce((obj, key) => {
        obj[ItemEnum[key]] = key;
        return obj;
    }, {});

    const renderTypes = (types) => {
        return types.map(typeId => {
            const itemName = REVERSED_ITEM_ENUM[typeId];
            return (
                <MenuItem 
                    key={typeId} 
                    // Pass both typeId and the itemType as 'type' to the handler
                    onClick={() => handleSidebarClick(typeId, 'type')}
                >
                    {itemName} 
                </MenuItem>
            );
        });
    };

    const renderSidebarItem = (group) => {
        return (
            <SubMenu
                key={group.market_group_id}
                title={group.name}
                icon={<img src={group.iconFile} alt={group.name} style={{ width: '32px', height: '32px' }} />}
                // Pass both market_group_id and the itemType as 'group' to the handler
                onClick={() => handleSidebarClick(group.market_group_id, 'group')}
            >
                {renderTypes(group.types)}
                {group.children.map(childGroup => renderSidebarItem(childGroup))}
            </SubMenu>
        );
    };

    return (
        <ProSidebar>
            <Menu>
                {marketGroupsJSON.map(renderSidebarItem)}
            </Menu>
        </ProSidebar>
    );
};

export default CustomSidebar;
