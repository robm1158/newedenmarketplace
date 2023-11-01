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

    // Given that types are now just an array of numbers, 
    // we don't have the name of the type in the structure anymore.
    // So, we'll render the number as a placeholder.
    const renderTypes = (types) => {
        return types.map(typeId => {
            const itemName = REVERSED_ITEM_ENUM[typeId]; // Map typeId to its name
            return (
                <MenuItem 
                    key={typeId} 
                    onClick={() => handleSidebarClick(typeId)}
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
