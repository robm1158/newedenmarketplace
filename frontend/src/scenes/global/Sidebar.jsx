import 'react-pro-sidebar/dist/css/styles.css';
import React from 'react';
import { ProSidebar, Menu, MenuItem, SubMenu } from 'react-pro-sidebar';
import marketGroupsJSON from '/root/code/eve-aws/frontend/src/constants/marketGroups.json';

const CustomSidebar = ({ handleSidebarClick }) => {

    // Given that types are now just an array of numbers, 
    // we don't have the name of the type in the structure anymore.
    // So, we'll render the number as a placeholder.
    const renderTypes = (types) => {
        console.log("Rendering types:", types);
        return types.map(typeId => (
            <MenuItem 
                key={typeId} 
                onClick={() => handleSidebarClick(typeId)}
            >
                {typeId} {/* placeholder for the type's name */}
            </MenuItem>
        ));
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
